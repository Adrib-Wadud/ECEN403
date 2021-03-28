from time import sleep
import sys
 
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class LCD:
    def __init__(self, pixelWidth=128, pixelHeight=32, padding=-2):
        #saving passed screen width and height
        self.pixelWidth = pixelWidth
        self.pixelHeight = pixelHeight
        
        #initialize I2C interface
        self.i2c = busio.I2C(board.SCL, board.SDA)
         
        #initialize display with pixel width, pixel height, and I2C interface
        self.disp = adafruit_ssd1306.SSD1306_I2C(pixelWidth, pixelHeight, self.i2c)

        #clear display
        self.disp.fill(0)
        self.disp.show()
         
        #create blank image for drawing
        self.image = Image.new("1", (pixelWidth, pixelHeight)) #"1" = 1-bit color
         
        #intialize drawing object to enable drawing
        self.draw = ImageDraw.Draw(self.image)
         
        #define vertical limits of screen
        self.top = padding
        self.bottom = pixelHeight - padding
         
        #load default font
        self.font = ImageFont.load_default()
    
    def displaySystemData(self, temperature = 0, humidity = 0, fanSpeed = 0,
                    humidifierIntensity = 0, tempSetting = 0,
                    humidityCap = 0, batteryLevel = 100, autoMode = 1):
        #draw black rectangle to clear image
        self.draw.rectangle((0, 0, self.pixelWidth, self.pixelHeight), outline=0, fill=0)
        
        #construct first text line with temp left-adjusted and battery level right-adjusted
        halfLine1 = "Temp:" + str(temperature) + u"\N{DEGREE SIGN}C"
        halfLine2 = "Batt:" + str(batteryLevel)
        firstLine = str(halfLine1) + (((self.pixelWidth//6) - len(halfLine1) - len(halfLine2))*" ") + str(halfLine2) #6-pixel character width
        
        #write relevent system data to image
        self.draw.text((0, self.top + 0), firstLine, font=self.font, fill=255)
        self.draw.text((0, self.top + 8), "Humidity:" + str(humidity), font=self.font, fill=255)
        #check current operation mode and display corresponding information
        if(not autoMode):
            self.draw.text((0, self.top + 16), "Fan Speed:" + str(fanSpeed), font=self.font, fill=255)
            self.draw.text((0, self.top + 24), "Humidifier:" + str(humidifierIntensity), font=self.font, fill=255)
        elif(autoMode):
            self.draw.text((0, self.top + 16), "Desired Temp:" + str(tempSetting), font=self.font, fill=255)
            self.draw.text((0, self.top + 24), "Humidity Cap:" + str(humidityCap), font=self.font, fill=255)
        
        #display image
        self.disp.image(self.image)
        self.disp.show()