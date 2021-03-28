from gpiozero import Button
from signal import pause
import sys
from physicalInputAssemblage import physicalInputAssemblage

physicalInput = physicalInputAssemblage()

#wiring buttons to GPIO pins (use "J8:##" for BOARD numbers, gpiozero defaults to BCM numbers)
fan_TempUpButton = Button("J8:11")
fan_TempDownButton = Button("J8:13")
humidifier_HumidityUpButton = Button("J8:16")
humidifier_HumidityDownButton = Button("J8:15")

#wiring switch to GPIO pins
manualAutoSwitch = Button("J8:18")

#check switch starting position
if (manualAutoSwitch.is_pressed): #reading initial position of the mode switch
	physicalInput.switchToAuto()

try:
	#performing button specific increments/decrements on button press events
	fan_TempUpButton.when_pressed = physicalInput.incrementFan_Temp
	fan_TempDownButton.when_pressed = physicalInput.decrementFan_Temp
	humidifier_HumidityUpButton.when_pressed = physicalInput.incrementHumidifier_Humidity
	humidifier_HumidityDownButton.when_pressed = physicalInput.decrementHumidifier_Humidity
	manualAutoSwitch.when_pressed = physicalInput.switchToAuto
	manualAutoSwitch.when_released = physicalInput.switchToManual

	pause() #wait for monitored signal events

except KeyboardInterrupt: #allow user to terminate program with ctrl + c
	sys.exit("Program Terminated")