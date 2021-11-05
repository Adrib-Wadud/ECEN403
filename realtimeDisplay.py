from MCP3008 import MCP3008
from physicalInputAssemblage import physicalInputAssemblage
from LCD import LCD
from cooling_subsystem_refined import manual_control, auto_control
#import bluetooth_server_

from time import time, sleep
from RPi.GPIO import cleanup 
from sys import exit

SENSOR_UPDATE_TIME = 1 #seconds
LCD_UPDATE_TIME = 0.1 #seconds

#initialize all button and switch functionality
physicalInput = physicalInputAssemblage()

#instantiate LCD object
lcd = LCD()

#initialize ADC
adc = MCP3008()

#define variables for use in main program loop
temperatureChannel = 0 #ADC channel connected to temp sensor
temperatureSum = 0 #running sum of temp sensor readings (averaged to smooth sensor output)
humidityChannel = 1 #ADC channel connected to humidity sensor
humiditySum = 0 #running sum of humidity sensor readings (averaged to smooth sensor output)

numReadings = 0 #count of readings (used when averaging sensor voltage output)
pastSensorTime = time() #save time to allow timing of sensor/LCD updates
pastLcdTime = time()

#set initial temperature and humidity readings
temperature = round(adc.getTemperature(temperatureChannel), 1) #reporting temperature reading to one decimal place
humidity = round(adc.getHumidity(humidityChannel), 1) #reporting humidity reading to one decimal place
# temperature = 0
# humidity= 0
#placeholder for Nanda's code
batteryLevel = 50
batteryVoltage = 1
batteryAmperage = 2
panelVoltage = 3
panelWattage = 4

fan_speed_map = {0: 0, 25: 1, 50: 2, 75: 3, 100:4}

while True:
    try:
        #performing button specific increments/decrements on button press events
        physicalInput.fan_TempUpButton.when_pressed = physicalInput.incrementFan_Temp
        physicalInput.fan_TempDownButton.when_pressed = physicalInput.decrementFan_Temp
        physicalInput.humidifier_HumidityUpButton.when_pressed = physicalInput.incrementHumidifier_Humidity
        physicalInput.humidifier_HumidityDownButton.when_pressed = physicalInput.decrementHumidifier_Humidity
        physicalInput.toggleDisplayButton.when_pressed = physicalInput.toggleDisplay
        physicalInput.manualAutoSwitch.when_pressed = physicalInput.switchToAuto
        physicalInput.manualAutoSwitch.when_released = physicalInput.switchToManual
        
        #Sensor Reading Updates
        #counting number of temperature and humidity readings and adding to individual sums in preparation for averaging
        temperatureSum += adc.getTemperature(temperatureChannel)
        humiditySum += adc.getHumidity(humidityChannel)
        numReadings += 1
        
        #after every second, calculate sensor data averages
        presentTime = time()
        if((presentTime - pastSensorTime) >= SENSOR_UPDATE_TIME):
            #average temperature and humidity readings and round to one decimal place
            temperature = round(temperatureSum / numReadings, 1)
            humidity = round(humiditySum / numReadings, 1)
            
            #reset variables used for 1 second averaging
            temperatureSum, humiditySum, numReadings = 0, 0, 0
            pastSensorTime = presentTime
        
        #LCD Screen Updates
        if((presentTime - pastLcdTime) >= LCD_UPDATE_TIME): #after every 0.1 second, update LCD display
                                                               #data on screen depending on selected mode
            lcd.displaySystemData(temperature, humidity, physicalInput.fanSpeed,  #write new display text to LCD
                    physicalInput.humidifierIntensity, physicalInput.tempSetting,
                    physicalInput.humidityCap, physicalInput.displayScreen,
                    physicalInput.autoMode, batteryLevel, batteryVoltage,
                    batteryAmperage, panelVoltage, panelWattage)
            
            if physicalInput.autoMode == 0:
                manual_control(fan_speed_map[physicalInput.fanSpeed], physicalInput.humidifierIntensity)
            else:
                auto_control(temperature, physicalInput.tempSetting, humidity, physicalInput.humidityCap)
            
    except KeyboardInterrupt: #allow user to terminate program with ctrl + c
        #lcd.lcd.clear()  #clear LCD
        GPIO.output(6, 1)
        GPIO.output(13, 1)
        GPIO.output(19, 1)
        GPIO.output(26, 1)
        manual_control(0,0)
        cleanup()  #set all output pins back to input pins
        
        exit("Program Terminated")
