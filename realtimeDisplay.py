from MCP3008 import MCP3008
from physicalInputAssemblage import physicalInputAssemblage
from LCD_Class import LCD

from gpiozero import Button
from time import time, sleep
from sys import exit

SENSOR_UPDATE_TIME = 1 #seconds
LCD_UPDATE_TIME = 0.1 #seconds

#Human/Device Interaction Subsystem
#initialize physical user interface
physicalInput = physicalInputAssemblage()

#wiring buttons to GPIO pins (use "J8:##" for BOARD numbers, gpiozero defaults to BCM numbers)
fan_TempUpButton = Button("J8:11")
fan_TempDownButton = Button("J8:13")
humidifier_HumidityUpButton = Button("J8:16")
humidifier_HumidityDownButton = Button("J8:15")

#wiring switch to GPIO pins
manualAutoSwitch = Button("J8:18")

#check switch starting position
if (manualAutoSwitch.is_pressed): #reading initial position of the mode switch
	physicalInput.switchToAuto()


#initialize LCD
lcd = LCD()
pastLCDTime = time() #save time to allow LCD to be updated every 0.1s


#Sensor Subsystem
#initialize ADC
adc = MCP3008()

#defining variables for use in main program loop
tempChannel = 0 #ADC channel connected to temp sensor
tempVoltageSum = 0 #running sum of temp sensor voltage readings (averaged to smooth sensor voltage output)
numReadings = 0 #count of readings (used when averaging sensor voltage output)
pastSensorTime = time() #save time to allow sensor reading averages to be output every second

#set initial temperature and voltage readings
tempVoltage = adc.getVoltage(tempChannel)
temperature = adc.convertToTemp(tempVoltage, 1)
#placeholder for humidity sensor incorporation
humidity = 50


#placeholder for Nanda's code
batteryLevel = 50

while True:
    try:
        #Human/Device Interaction Subsystem
        #performing button specific increments/decrements on button press events
        fan_TempUpButton.when_pressed = physicalInput.incrementFan_Temp
        fan_TempDownButton.when_pressed = physicalInput.decrementFan_Temp
        humidifier_HumidityUpButton.when_pressed = physicalInput.incrementHumidifier_Humidity
        humidifier_HumidityDownButton.when_pressed = physicalInput.decrementHumidifier_Humidity
        manualAutoSwitch.when_pressed = physicalInput.switchToAuto
        manualAutoSwitch.when_released = physicalInput.switchToManual
        
        
        #Sensor Subsystem
        #counting each voltage reading and adding to sum in preparation for averaging
        tempVoltage = adc.getVoltage(tempChannel)
        tempVoltageSum += tempVoltage
        numReadings += 1
        
        presentTime = time()
        if((presentTime - pastSensorTime) >= SENSOR_UPDATE_TIME): #after every second, calculate sensor data averages
            #average temperature sensor voltage output and convert to temperature reading
            averageTempVoltage = tempVoltageSum / numReadings
            temperature = adc.convertToTemp(averageTempVoltage, 1)
            
            #reset variables used for 1 second averaging
            tempVoltageSum, numReadings = 0, 0
            pastSensorTime = presentTime
        
        
        if((presentTime - pastSensorTime) >= LCD_UPDATE_TIME): #after every 0.1 second, update LCD
            #display data on screen depending on selected mode
            lcd.displaySystemData(temperature, humidity, physicalInput.fanSpeed,
                    physicalInput.humidifierIntensity, physicalInput.tempSetting,
                    physicalInput.humidityCap, batteryLevel, physicalInput.autoMode)
        
    except KeyboardInterrupt: #allow user to terminate program with ctrl + c
        #clear screen
        lcd.disp.fill(0)
        lcd.disp.show()
        
        exit("Program Terminated")