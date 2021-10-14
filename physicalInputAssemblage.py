from gpiozero import Button
from time import time, sleep


class physicalInputAssemblage:
    MAX_FAN_SPEED = 100
    MAX_HUMIDIFIER_INTENSITY = 3
    MAX_TEMP_SETTING = 35  # degrees celcius
    MAX_HUMIDITY_CAP = 100  # %RH
    BUTTON_DEBOUNCE_TIME = 0.1  # 100ms

    def __init__(self, fanSpeed=0, humidifierIntensity=0,
                 tempSetting=25, humidityCap=50, autoMode=0,
                 displayScreen=0):

        # setting initial class attribute values
        self.fanSpeed = fanSpeed
        self.humidifierIntensity = humidifierIntensity
        self.tempSetting = tempSetting
        self.humidityCap = humidityCap
        self.autoMode = autoMode
        self.displayScreen = displayScreen

        self.lastUpdateTime = time()  # save to start counting seconds to next button press

        # wiring buttons to GPIO pins (use "J8:##" for BOARD numbers, gpiozero defaults to BCM numbers)
        # on/off button is wired in pi /boot/config text. CHANGE TO PIN 7 FOR FINAL PCB
        self.fan_TempUpButton = Button("J8:16")  # CHANGE TO PIN 13 FOR FINAL PCB
        self.fan_TempDownButton = Button("J8:18")  # CHANGE TO PIN 38 FOR FINAL PCB
        self.humidifier_HumidityUpButton = Button("J8:13")  # CHANGE TO PIN 15 FOR FINAL PCB
        self.humidifier_HumidityDownButton = Button("J8:11")  # CHANGE TO PIN 40 FOR FINAL PCB
        self.toggleDisplayButton = Button("J8:36")

        # wiring mode select switch to GPIO pins
        self.manualAutoSwitch = Button("J8:22")  # CHANGE TO PIN 11 FOR FINAL PCB

        # check switch starting position
        if self.manualAutoSwitch.is_pressed:  # reading initial position of the mode switch
            self.switchToAuto()

    def incrementFan_Temp(self):  # increments fan speed/temperature setting (up to max)
        if (time() - self.lastUpdateTime) >= self.BUTTON_DEBOUNCE_TIME:  # handles button debounce
            if not self.autoMode:  # Manual mode button functionality
                if self.fanSpeed < self.MAX_FAN_SPEED:  # increment as long as speed is below max
                    self.fanSpeed += 25
            elif self.autoMode:  # Auto mode button functionality
                if self.tempSetting < self.MAX_TEMP_SETTING:  # increment as long as temp setting is below max
                    self.tempSetting += 1

            self.lastUpdateTime = time()  # save to start counting seconds to next button press

    def decrementFan_Temp(self):  # decrements fan speed/temperature setting (0 minimum)
        if (time() - self.lastUpdateTime) >= self.BUTTON_DEBOUNCE_TIME:  # handles button debounce
            if not self.autoMode:  # Manual mode button functionality
                if self.fanSpeed > 0:  # decrement as long as speed is above 0
                    self.fanSpeed -= 25
            elif self.autoMode:  # Auto mode button functionality
                if self.tempSetting > 0:  # decrement as long as temp setting is above 0
                    self.tempSetting -= 1

            self.lastUpdateTime = time()  # save to start counting seconds to next button press

    def incrementHumidifier_Humidity(self):  # increments humidifier intensity/humidity Cap (up to max)
        if (time() - self.lastUpdateTime) >= self.BUTTON_DEBOUNCE_TIME:  # handles button debounce
            if not self.autoMode:  # Manual mode button functionality
                if self.humidifierIntensity < self.MAX_HUMIDIFIER_INTENSITY:  # increment as long as intensity is below max
                    self.humidifierIntensity += 1
            elif self.autoMode:  # Auto mode button functionality
                if self.humidityCap < self.MAX_HUMIDITY_CAP:  # increment as long as humidity cap is below max
                    self.humidityCap += 1

            self.lastUpdateTime = time()  # save to start counting seconds to next button press

    def decrementHumidifier_Humidity(self):  # decrements humidifier intensity/humidity Cap (0 minimum)
        if (time() - self.lastUpdateTime) >= self.BUTTON_DEBOUNCE_TIME:  # handles button debounce
            if not self.autoMode:  # Manual mode button functionality
                if self.humidifierIntensity > 0:  # increment as long as intensity is above 0
                    self.humidifierIntensity -= 1
            elif self.autoMode:  # Auto mode button functionality
                if self.humidityCap > 0:  # increment as long as humidity cap is above 0
                    self.humidityCap -= 1

            self.lastUpdateTime = time()  # save to start counting seconds to next button press

    def toggleDisplay(self):  # toggles value of displayScreen to switch between
        # user settings and charge controller info screens
        if (time() - self.lastUpdateTime) >= self.BUTTON_DEBOUNCE_TIME:  # handles button debounce
            self.displayScreen ^= 1

        self.lastUpdateTime = time()  # save to start counting seconds to next button press

    def switchToManual(self):  # sets autoMode to 0 (enables manual mode)
        self.autoMode = 0

    def switchToAuto(self):  # sets autoMode to 1 (enables auto mode)
        self.autoMode = 1
