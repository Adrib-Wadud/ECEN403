import sys
from physicalInputAssemblage import physicalInputAssemblage

#initialize physical user interface
physicalInput = physicalInputAssemblage()

try:
    while True:
        #performing button specific increments/decrements on button press events
        physicalInput.fan_TempUpButton.when_pressed = physicalInput.incrementFan_Temp
        physicalInput.fan_TempDownButton.when_pressed = physicalInput.decrementFan_Temp
        physicalInput.humidifier_HumidityUpButton.when_pressed = physicalInput.incrementHumidifier_Humidity
        physicalInput.humidifier_HumidityDownButton.when_pressed = physicalInput.decrementHumidifier_Humidity
        physicalInput.manualAutoSwitch.when_pressed = physicalInput.switchToAuto
        physicalInput.manualAutoSwitch.when_released = physicalInput.switchToManual

except KeyboardInterrupt: #allow user to terminate program with ctrl + c
	sys.exit("Program Terminated")