from MCP3008 import MCP3008
from physicalInputAssemblage import physicalInputAssemblage
from LCD import LCD

from time import time
from sys import exit

SENSOR_UPDATE_TIME = 1 #seconds
LCD_UPDATE_TIME = 0.1 #seconds

#Human/Device Interaction Subsystem
#initialize physical user interface
physicalInput = physicalInputAssemblage()

#instantiate LCD object
lcd = LCD()


#Sensor Subsystem
#initialize ADC
adc = MCP3008()

#defining variables for use in main program loop
temperatureChannel = 0 #ADC channel connected to temp sensor
temperatureSum = 0 #running sum of temp sensor readings (averaged to smooth sensor output)

humidityChannel = 1 #ADC channel connected to humidity sensor
humiditySum = 0 #running sum of humidity sensor readings (averaged to smooth sensor output)

numReadings = 0 #count of readings (used when averaging sensor voltage output)
pastSensorTime = time() #save time to allow sensor reading averages to be output every second

#set initial temperature and humidity readings
temperature = round(adc.getTemperature(temperatureChannel), 1) #reporting temperature reading to one decimal place
humidity = round(adc.getHumidity(humidityChannel, temperature), 1) #reporting humidity reading to one decimal place

#placeholder for Nanda's code
batteryLevel = 50

while True:
    try:
        #Physical Button Assemblage
        #performing button specific increments/decrements on button press events
        physicalInput.fan_TempUpButton.when_pressed = physicalInput.incrementFan_Temp
        physicalInput.fan_TempDownButton.when_pressed = physicalInput.decrementFan_Temp
        physicalInput.humidifier_HumidityUpButton.when_pressed = physicalInput.incrementHumidifier_Humidity
        physicalInput.humidifier_HumidityDownButton.when_pressed = physicalInput.decrementHumidifier_Humidity
        physicalInput.manualAutoSwitch.when_pressed = physicalInput.switchToAuto
        physicalInput.manualAutoSwitch.when_released = physicalInput.switchToManual
        
        
        #Sensor Reading Updates
        #counting each temperature and humidity reading and adding to individual sums in preparation for averaging
        currentTemperature = adc.getTemperature(temperatureChannel)
        temperatureSum += currentTemperature
        currentHumidity = adc.getHumidity(humidityChannel, currentTemperature)
        humiditySum += currentHumidity
        numReadings += 1
        
        presentTime = time()
        if((presentTime - pastSensorTime) >= SENSOR_UPDATE_TIME): #after every second, calculate sensor data averages
            #average temperature and humidity readings and round to one decimal place
            temperature = round(temperatureSum / numReadings, 1)
            humidity = round(humiditySum / numReadings, 1)
            
            #reset variables used for 1 second averaging
            temperatureSum, humiditySum, numReadings = 0, 0, 0
            pastSensorTime = presentTime
        
        
        #LCD Screen Updates
        if((presentTime - pastSensorTime) >= LCD_UPDATE_TIME): #after every 0.1 second, update LCD
            #display data on screen depending on selected mode
            lcd.displaySystemData(temperature, humidity, physicalInput.fanSpeed,
                    physicalInput.humidifierIntensity, physicalInput.tempSetting,
                    physicalInput.humidityCap, batteryLevel, physicalInput.autoMode)
        
    except KeyboardInterrupt: #allow user to terminate program with ctrl + c
        #clear screen
        lcd.lcd.clear()
        
        exit("Program Terminated")
