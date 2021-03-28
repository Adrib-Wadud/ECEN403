class physicalInputAssemblage:
    
    MAX_FAN_SPEED = 4
    MAX_HUMIDIFIER_INTENSITY = 4
    MAX_TEMP_SETTING = 100 #degrees fahrenheit
    MAX_HUMIDITY_CAP = 100 #percent RH
    
    def __init__(self, fanSpeed = 0, humidifierIntensity = 0, tempSetting = 0, humidityCap = 0, autoMode = 0):
        self.fanSpeed = fanSpeed
        self.humidifierIntensity = humidifierIntensity
        self.tempSetting = tempSetting
        self.humidityCap = humidityCap
        self.autoMode = autoMode
        
    def incrementFan_Temp(self): #increments fan speed/temperature setting (up to max)
        if (not self.autoMode): #Manual mode button functionality
            if (self.fanSpeed < self.MAX_FAN_SPEED): #increment as long as speed is below max
                self.fanSpeed += 1
                print("fanSpeed = ", self.fanSpeed)

        elif (self.autoMode): #Auto mode button functionality
            if (self.tempSetting < self.MAX_TEMP_SETTING): #increment as long as temp setting is below max
                self.tempSetting += 1
                print("tempSetting = ", self.tempSetting)

    def decrementFan_Temp(self): #decrements fan speed/temperature setting (0 minimum)
        if (not self.autoMode): #Manual mode button functionality
            if (self.fanSpeed > 0): #decrement as long as speed is above 0
                self.fanSpeed -= 1
                print("fanSpeed = ", self.fanSpeed)

        elif (self.autoMode): #Auto mode button functionality
            if (self.tempSetting > 0): #decrement as long as temp setting is above 0
                self.tempSetting -= 1
                print("tempSetting = ", self.tempSetting)

    def incrementHumidifier_Humidity(self): #increments humidifier intensity/humidity Cap (up to max)
        if (not self.autoMode): #Manual mode button functionality
            if (self.humidifierIntensity < self.MAX_HUMIDIFIER_INTENSITY): #increment as long as intensity is below max
                self.humidifierIntensity += 1
                print("humidifierIntensity  = ", self.humidifierIntensity)

        elif (self.autoMode): #Auto mode button functionality
            if (self.humidityCap < self.MAX_HUMIDITY_CAP): #increment as long as humidity cap is below max
                self.humidityCap += 1
                print("humidityCap = ", self.humidityCap)

    def decrementHumidifier_Humidity(self): #decrements humidifier intensity/humidity Cap (0 minimum)
        if (not self.autoMode): #Manual mode button functionality
            if (self.humidifierIntensity > 0): #increment as long as intensity is above 0
                self.humidifierIntensity -= 1
                print("humidifierIntensity  = ", self.humidifierIntensity)

        elif (self.autoMode): #Auto mode button functionality
            if (self.humidityCap > 0): #increment as long as humidity cap is above 0
                self.humidityCap -= 1
                print("humidityCap = ", self.humidityCap)

    def switchToManual(self):
        self.autoMode = 0
        print("Manual Mode Entered")

    def switchToAuto(self):
        self.autoMode = 1
        print("Auto Mode Entered")