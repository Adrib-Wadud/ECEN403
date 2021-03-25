from gpiozero import Button
from signal import pause
import sys

MAX_FAN_SPEED = 4
MAX_HUMIDIFIER_INTENSITY = 4
MAX_TEMP_SETTING = 100 #degrees fahrenheit
MAX_HUMIDITY_CAP = 100 #percent RH

#wiring buttons to GPIO pins (use "J8:##" for BOARD numbers, gpiozero defaults to BCM numbers)
fan_TempUpButton = Button("J8:11")
fan_TempDownButton = Button("J8:13")
humidifier_HumidityUpButton = Button("J8:16")
humidifier_HumidityDownButton = Button("J8:15")

#wiring switch to GPIO pins
switchAutoPosition = Button("J8:18")

#defining global variables
fanSpeed = 0
humidifierIntensity = 0
tempSetting = 0
humidityCap = 0
if (switchAutoPosition.is_pressed): #reading initial position of the mode switch
	autoMode = 1
else:
	autoMode = 0

def incrementFan_Temp(): #increments fan speed/temperature setting (up to max)
	#specifying global variables to use
	global fanSpeed
	global tempSetting

	if (not autoMode): #Manual mode button functionality
		if (fanSpeed < MAX_FAN_SPEED): #increment as long as speed is below max
			fanSpeed = fanSpeed + 1
			print("fanSpeed = ", fanSpeed)

	elif (autoMode): #Auto mode button functionality
		if (tempSetting < MAX_TEMP_SETTING): #increment as long as temp setting is below max
			tempSetting = tempSetting + 1
			print("tempSetting = ", tempSetting)

def decrementFan_Temp(): #decrements fan speed/temperature setting (0 minimum)
	#specifying global variables to use
	global fanSpeed
	global tempSetting

	if (not autoMode): #Manual mode button functionality
		if (fanSpeed > 0): #decrement as long as speed is above 0
			fanSpeed = fanSpeed - 1
			print("fanSpeed = ", fanSpeed)

	elif (autoMode): #Auto mode button functionality
		if (tempSetting > 0): #decrement as long as temp setting is above 0
			tempSetting = tempSetting - 1
			print("tempSetting = ", tempSetting)

def incrementHumidifier_Humidity(): #increments humidifier intensity/humidity Cap (up to max)
	#specifying global variables to use
	global humidifierIntensity
	global humidityCap

	if (not autoMode): #Manual mode button functionality
		if (humidifierIntensity < MAX_HUMIDIFIER_INTENSITY): #increment as long as intensity is below max
			humidifierIntensity = humidifierIntensity + 1
			print("humidifierIntensity  = ", humidifierIntensity)

	elif (autoMode): #Auto mode button functionality
		if (humidityCap < MAX_HUMIDITY_CAP): #increment as long as humidity cap is below max
			humidityCap = humidityCap + 1
			print("humidityCap = ", humidityCap)

def decrementHumidifier_Humidity(): #decrements humidifier intensity/humidity Cap (0 minimum)
	#specifying global variables to use
	global humidifierIntensity
	global humidityCap

	if (not autoMode): #Manual mode button functionality
		if (humidifierIntensity > 0): #increment as long as intensity is above 0
			humidifierIntensity = humidifierIntensity - 1
			print("humidifierIntensity  = ", humidifierIntensity)

	elif (autoMode): #Auto mode button functionality
		if (humidityCap > 0): #increment as long as humidity cap is above 0
			humidityCap = humidityCap - 1
			print("humidityCap = ", humidityCap)

def switchToManual():
	global autoMode
	autoMode = 0
	print("Manual Mode Entered")

def switchToAuto():
	global autoMode
	autoMode = 1
	print("Auto Mode Entered")

try:
	#performing button specific increments/decrements on button press events
	fan_TempUpButton.when_pressed = incrementFan_Temp
	fan_TempDownButton.when_pressed = decrementFan_Temp
	humidifier_HumidityUpButton.when_pressed = incrementHumidifier_Humidity
	humidifier_HumidityDownButton.when_pressed = decrementHumidifier_Humidity
	switchAutoPosition.when_pressed = switchToAuto
	switchAutoPosition.when_released = switchToManual

	pause() #wait for monitored signal events

except KeyboardInterrupt: #allow user to terminate program with ctrl + c
	sys.exit("Program Terminated")
