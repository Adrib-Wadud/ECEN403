from MCP3008 import MCP3008
from physicalInputAssemblage_func import physicalInputAssemblage
from LCD import LCD
from cooling_subsystem_refined import manual_control, auto_control
from renogywanderer import get_power_data

from time import time, sleep
from RPi.GPIO import cleanup 
from sys import exit


def real_display(FS, HI, power_data, TS, HS, p_list, C_L, B_V, B_A, P_A, P_W):
    
    SENSOR_UPDATE_TIME = 1 #seconds
    LCD_UPDATE_TIME = 0.1 #seconds
    #initialize all button and switch functionality
    #physicalInput = physicalInputAssemblage(F_S= FS, H_I=HI, T_S=TS, H_S=HS, power_data)
    physicalInput = physicalInputAssemblage(F_S= FS, H_I=HI, T_S=TS, H_S=HS, power_data=power_data)

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

    fan_speed_map = {0: 0, 25: 1, 50: 2, 75: 3, 100:4}
    f_m = {0: 0, 1: 25, 2: 50, 3: 75, 4:100}
    manual_control(0,0)
    
    #power_data.batteryLevel = 80
    #power_data.panelAmperage = 100.0
    while True:
        try:
            power_metric = get_power_data()
            p_list = power_metric
            C_L.value = power_metric[4]
            B_V.value = power_metric[0]
            B_A.value = power_metric[1]
            P_A.value = power_metric[2]
            P_W.value = power_metric[3]
            power_data.batteryLevel = power_metric[4]
            power_data.batteryVoltage = power_metric[0]
            power_data.batteryAmperage = power_metric[1]
            power_data.panelAmperage = power_metric[2]
            power_data.panelWattage = power_metric[3]
            
            if power_data.batteryLevel <= 20:
                physicalInput.MODE = 'Low'
        except:
            pass
        
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
                        physicalInput.autoMode, power_data.batteryLevel, power_data.batteryVoltage,
                        power_data.batteryAmperage, power_data.panelAmperage, power_data.panelWattage)
                
                if physicalInput.autoMode == 0:
                    physicalInput.fanSpeed = f_m[FS.value]
                    print('PHYS FS: ' +str(FS.value))
                    #print(physicalInput.fanSpeed)
                    physicalInput.humidifierIntensity = HI.value
                    print('PHYS HI: ' +str(HI.value))
                    if physicalInput.MODE == 'Low':
                        if physicalInput.fanSpeed > 50:
                            FS.value = 2
                            physicalInput.fanSpeed = f_m[FS.value]
                        if physicalInput.humidifierIntensity > 1:
                            HI.value = 1
                            physicalInput.humidifierIntensity = HI.value
                    
                    manual_control(fan_speed_map[physicalInput.fanSpeed], physicalInput.humidifierIntensity)
                else:
                    physicalInput.tempSetting = TS.value
                    physicalInput.humidityCap = HS.value
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
