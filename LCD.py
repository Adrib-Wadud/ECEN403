from Adafruit_CharLCD import Adafruit_CharLCD
import Adafruit_GPIO.PCF8574 as PCF
from time import sleep

class LCD:
    def __init__(self, address=0x20, lcdRS=4, lcdEN=6, D4=0,
                 D5=1, D6=2, D7=3, columns=20, lines=4):
        self.GPIO = PCF.PCF8574(address) #instantiating PCF object using adress of PFC

        self.columns = columns
        self.lines = lines

        #instantiate LCD object
        self.lcd = Adafruit_CharLCD(lcdRS, lcdEN, D4, D5, D6, D7,
                                   columns, lines, gpio=self.GPIO)

        #clearing LCD
        self.lcd.clear()
        
    def displaySystemData(self, temperature, humidity, fanSpeed,
                        humidifierIntensity, tempSetting,
                        humidityCap, batteryLevel, autoMode):
        
        #construct first text line with temp left-adjusted and battery level right-adjusted
        halfLine1 = "Temp:" + str(temperature) + "C"
        halfLine2 = "Batt:" + str(batteryLevel)
        firstLine = str(halfLine1) + (self.columns - len(halfLine1) - len(halfLine2))*" " + str(halfLine2) #6-pixel character width
        
        secondLine = "Humidity:" + str(humidity)
        secondLine += (self.columns - len(secondLine))*" " #formatting to write over previous text when function is called
        
        #check current operation mode and display corresponding information
        if(not autoMode):
            thirdLine = "Fan Speed:" + str(fanSpeed)
            fourthLine = "Humidifier:" + str(humidifierIntensity)
            
        elif(autoMode):
            thirdLine ="Desired Temp:" + str(tempSetting)
            fourthLine = "Humidity Cap:" + str(humidityCap)
            
        thirdLine += (self.columns - len(thirdLine))*" "
        fourthLine += (self.columns - len(fourthLine))*" "
        
        #write relevent system data to screen
        self.lcd.set_cursor(0,0)
        self.lcd.message(firstLine)
        self.lcd.set_cursor(0,1)
        self.lcd.message(secondLine)
        self.lcd.set_cursor(0,2)
        self.lcd.message(thirdLine)
        self.lcd.set_cursor(0,3)
        self.lcd.message(fourthLine)