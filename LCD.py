import time
import sys
import subprocess
 
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
 
 
# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
 
# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
 
# Clear display.
disp.fill(0)
disp.show()
 
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
#draw.rectangle((0, 0, width, height), outline=0, fill=0)
 
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
 
# Load default font.
font = ImageFont.load_default()
 
# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)
 
temperature = 25.1
humidity = 50
fanSpeed = 0
humidifierIntensity = 0
tempSetting = 0
humidityCap = 0
batteryLevel = 100
autoMode = 1
 
while True:
    try:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        
        halfLine1 = "Temp:" + str(temperature)
        halfLine2 = "Batt:" + str(batteryLevel)
        firstLine = str(halfLine1) + (((width//6) - len(halfLine1) - len(halfLine2))*" ") + str(halfLine2) #6-pixel character width
        # Write four lines of text.
        draw.text((0, top + 0), firstLine, font=font, fill=255)
        draw.text((0, top + 8), "Humidity:" + str(humidity), font=font, fill=255)
        # Check current operation mode and display corresponding information
        if(not autoMode):
            draw.text((0, top + 16), "Fan Speed:" + str(fanSpeed), font=font, fill=255)
            draw.text((0, top + 24), "Humidifier:" + str(humidifierIntensity), font=font, fill=255)
        elif(autoMode):
            draw.text((0, top + 16), "Desired Temp:" + str(tempSetting), font=font, fill=255)
            draw.text((0, top + 24), "Humidity Cap:" + str(humidityCap), font=font, fill=255)
        
        # Display image.
        disp.image(image)
        disp.show()
        time.sleep(0.1)
    
    except KeyboardInterrupt:
        disp.fill(0)
        disp.show()
        sys.exit("Program Terminated")
