from time import sleep
import sys
from LCD_Class import LCD

#initialize LCD
lcd = LCD()

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
        #display data on screen depending on selected mode
        lcd.displaySystemData(temperature, humidity, fanSpeed,
                    humidifierIntensity, tempSetting,
                    humidityCap, batteryLevel, autoMode)
        sleep(0.1) #update screen every 0.1s
        
    except KeyboardInterrupt: #allow user to terminate program with ctrl + c
        #clear screen
        lcd.disp.fill(0)
        lcd.disp.show()
        
        sys.exit("Program Terminated")