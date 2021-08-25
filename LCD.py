from Adafruit_CharLCD import Adafruit_CharLCD
import Adafruit_GPIO.PCF8574 as PCF
from time import sleep

class LCD:
    def __init__(self, address=0x20, lcdRS=4, lcdEN=6, D4=0,
                 D5=1, D6=2, D7=3, columns=20, lines=4):
        self.GPIO = PCF.PCF8574(address) #instantiating PCF object using adress of PFC

        #sets screen size constraints
        self.columns = columns
        self.lines = lines

        #instantiate LCD object
        self.lcd = Adafruit_CharLCD(lcdRS, lcdEN, D4, D5, D6, D7,
                                   columns, lines, gpio=self.GPIO)

        #clearing LCD
        self.lcd.clear()
        
    def displaySystemData(self, temperature, humidity, fanSpeed,  #updates LCD with current cooling system data
                        humidifierIntensity, tempSetting, humidityCap,
                        displayScreen, autoMode, batteryLevel,
                        batteryVoltage, batteryAmperage, panelVoltage,
                        panelWattage):
        
        if(displayScreen):  #if display screen 1 is selected, format charge controller data for display
            firstLine = "Batt Voltage:" + str(batteryVoltage) + "V"
            firstLine += (self.columns - len(firstLine))*" " #Ensuring all previous display text is overwritten
            secondLine = "Batt Amperage:" + str(batteryAmperage) + "A"
            secondLine += (self.columns - len(secondLine))*" " 
            thirdLine = "Panel Voltage:" + str(panelVoltage) + "V"
            thirdLine += (self.columns - len(thirdLine))*" " 
            fourthLine = "Panel Wattage:" + str(panelWattage) + "W"
            fourthLine += (self.columns - len(fourthLine))*" " 
        
        else: #if display screen 0 is selected, format user settings and climate data for display
            #construct first text line with temp left-adjusted and battery level right-adjusted
            halfLine1 = "Temp:" + str(temperature) + "C"
            halfLine2 = "Batt:" + str(batteryLevel) + "%"
            firstLine = str(halfLine1) + (self.columns - len(halfLine1) - len(halfLine2))*" " + str(halfLine2)
            
            secondLine = "Humidity:" + str(humidity) + "%RH"
            secondLine += (self.columns - len(secondLine))*" " #Ensuring all previous display text is overwritten
            
            #check current operation mode and display corresponding information
            if(not autoMode):  #if manual mode, show fan speed and humidifier intensity
                thirdLine = "Fan Speed:" + str(fanSpeed) + "%"
                fourthLine = "Humidifiers:" + str(humidifierIntensity)
                
            elif(autoMode):  #if auto mode, show desired temperature and humidity cap
                thirdLine ="Desired Temp:" + str(tempSetting) + "C"
                fourthLine = "Humidity Cap:" + str(humidityCap) + "%RH"
            
            #Ensuring all previous display text is overwritten
            thirdLine += (self.columns - len(thirdLine))*" "
            fourthLine += (self.columns - len(fourthLine))*" "
        
        #write relevent system data to screen
        self.lcd.set_cursor(0,0)  #moving cursor to the first column of row 0
        self.lcd.message(firstLine)  #writing a line of text to the LCD
        self.lcd.set_cursor(0,1)
        self.lcd.message(secondLine)
        self.lcd.set_cursor(0,2)
        self.lcd.message(thirdLine)
        self.lcd.set_cursor(0,3)
        self.lcd.message(fourthLine)
