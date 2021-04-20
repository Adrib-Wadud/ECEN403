from gpiozero import Button
from time import time, sleep

class physicalInputAssemblage:
    
    MAX_FAN_SPEED = 4
    MAX_HUMIDIFIER_INTENSITY = 4
    MAX_TEMP_SETTING = 100 #degrees fahrenheit
    MAX_HUMIDITY_CAP = 100 #percent RH
    BUTTON_DEBOUNCE_TIME = 0.1 #100ms
    
    def __init__(self, fanSpeed = 0, humidifierIntensity = 0, tempSetting = 0, humidityCap = 0, autoMode = 0):
        self.fanSpeed = fanSpeed
        self.humidifierIntensity = humidifierIntensity
        self.tempSetting = tempSetting
        self.humidityCap = humidityCap
        self.autoMode = autoMode
        
        self.lastUpdateTime = time() #save to start counting seconds to next button press
        
        #wiring buttons to GPIO pins (use "J8:##" for BOARD numbers, gpiozero defaults to BCM numbers)
        self.fan_TempUpButton = Button("J8:16")
        self.fan_TempDownButton = Button("J8:18")
        self.humidifier_HumidityUpButton = Button("J8:13")
        self.humidifier_HumidityDownButton = Button("J8:11")

        #wiring switch to GPIO pins
        self.manualAutoSwitch = Button("J8:22")

        #check switch starting position
        if (self.manualAutoSwitch.is_pressed): #reading initial position of the mode switch
            self.switchToAuto()
        
    def incrementFan_Temp(self): #increments fan speed/temperature setting (up to max)
        if ((time() - self.lastUpdateTime) >= self.BUTTON_DEBOUNCE_TIME): #handles button debounce
            if (not self.autoMode): #Manual mode button functionality
                if (self.fanSpeed < self.MAX_FAN_SPEED): #increment as long as speed is below max
                    self.fanSpeed += 1
                    self.debounceButton = 1 #variable to initiate button debounce after LCD update
                    #print("fanSpeed = ", self.fanSpeed)
            elif (self.autoMode): #Auto mode button functionality
                if (self.tempSetting < self.MAX_TEMP_SETTING): #increment as long as temp setting is below max
                    self.tempSetting += 1
                    self.debounceButton = 1 #variable to initiate button debounce after LCD update
                    #print("tempSetting = ", self.tempSetting)
                    
            self.lastUpdateTime = time() #save to start counting seconds to next button press

    def decrementFan_Temp(self): #decrements fan speed/temperature setting (0 minimum)
        if ((time() - self.lastUpdateTime) >= self.BUTTON_DEBOUNCE_TIME): #handles button debounce
            if (not self.autoMode): #Manual mode button functionality
                if (self.fanSpeed > 0): #decrement as long as speed is above 0
                    self.fanSpeed -= 1
                    self.debounceButton = 1 #variable to initiate button debounce after LCD update
                    #print("fanSpeed = ", self.fanSpeed)
            elif (self.autoMode): #Auto mode button functionality
                if (self.tempSetting > 0): #decrement as long as temp setting is above 0
                    self.tempSetting -= 1
                    self.debounceButton = 1 #variable to initiate button debounce after LCD update
                    #print("tempSetting = ", self.tempSetting)
                    
            self.lastUpdateTime = time() #save to start counting seconds to next button press

    def incrementHumidifier_Humidity(self): #increments humidifier intensity/humidity Cap (up to max)
        if ((time() - self.lastUpdateTime) >= self.BUTTON_DEBOUNCE_TIME): #handles button debounce
            if (not self.autoMode): #Manual mode button functionality
                if (self.humidifierIntensity < self.MAX_HUMIDIFIER_INTENSITY): #increment as long as intensity is below max
                    self.humidifierIntensity += 1
                    self.debounceButton = 1 #variable to initiate button debounce after LCD update
                    #print("humidifierIntensity  = ", self.humidifierIntensity)
            elif (self.autoMode): #Auto mode button functionality
                if (self.humidityCap < self.MAX_HUMIDITY_CAP): #increment as long as humidity cap is below max
                    self.humidityCap += 1
                    self.debounceButton = 1 #variable to initiate button debounce after LCD update
                    #print("humidityCap = ", self.humidityCap)

            self.lastUpdateTime = time() #save to start counting seconds to next button press

    def decrementHumidifier_Humidity(self): #decrements humidifier intensity/humidity Cap (0 minimum)
        if ((time() - self.lastUpdateTime) >= self.BUTTON_DEBOUNCE_TIME): #handles button debounce
            if (not self.autoMode): #Manual mode button functionality
                if (self.humidifierIntensity > 0): #increment as long as intensity is above 0
                    self.humidifierIntensity -= 1
                    self.debounceButton = 1 #variable to initiate button debounce after LCD update
                    #print("humidifierIntensity  = ", self.humidifierIntensity)
            elif (self.autoMode): #Auto mode button functionality
                if (self.humidityCap > 0): #increment as long as humidity cap is above 0
                    self.humidityCap -= 1
                    self.debounceButton = 1 #variable to initiate button debounce after LCD update
                    #print("humidityCap = ", self.humidityCap)
            
            self.lastUpdateTime = time() #save to start counting seconds to next button press

    def switchToManual(self):
        self.autoMode = 0
        self.debounceButton = 1 #variable to initiate button debounce after LCD update
        #print("Manual Mode Entered")

    def switchToAuto(self):
        self.autoMode = 1
        self.debounceButton = 1 #variable to initiate button debounce after LCD update
        #print("Auto Mode Entered")
