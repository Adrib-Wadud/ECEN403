import RPi.GPIO as GPIO
import time
import pigpio  # must type "sudo pigpiod" into command line to run this

pi = pigpio.pi()
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)#Fan ON/OFF
GPIO.setup(13, GPIO.OUT)# Humidifier 1
GPIO.setup(19, GPIO.OUT)# Humidifier 2
GPIO.setup(26, GPIO.OUT)# Humidifier 3
AutoMode = 0

# auto mode initializing
currentTemp = 0
tempSetting = 32  # initialize at highest temp setting
tempDifference = 0  # difference between current temp and temp setting (tempDifference = tempSetting - currentTemp)
tempRange_1 = range(1, 3, 1)  # 0-4 degrees from setting
tempRange_2 = range(4, 7, 1)  # 4-7 degrees from setting
tempRange_3 = range(8, 11, 1)  # 8-11 degrees from setting
tempRange_4 = range(11, 16, 1)  # 11-16 degrees from setting // Hotter than 16 degrees from setting sets fan to run at full speed.
currentHumidity = 100
humidityCap = 100  # initialize at highest humidity setting
humidityDifference = 0  # difference between current humidity and humidity setting (humidityDifference = humidityCap - currentHumidity)
humidityRange_1 = range(1, 5, 1)  # 0-5% away from cap
humidityRange_2 = range(6, 20, 1)  # 6-15% away from cap
humidityRange_3 = range(21, 50, 1)  # 16-50% away from cap // 100% - 50% humidity DIFFERENCE sets all humidifiers to be on

# manual mode initializing
fanSpeed = 1
humidifierIntensity = 3


def manual_control(fanSpeed, humidifierIntensity):
    # Manual Mode Code
    if fanSpeed == 0 :#Fan is OFF
        GPIO.output(6,1)
    elif fanSpeed == 1 :
        GPIO.output(6,0)#Speed 25% Duty Cycle
        pi.hardware_PWM(12, 25000, 250000)
    elif fanSpeed == 2 :
        GPIO.output(6,0)#Speed 50% Duty Cycle
        pi.hardware_PWM(12, 25000, 500000)
    elif fanSpeed == 3 :
        GPIO.output(6,0)#Speed 75% Duty Cycle
        pi.hardware_PWM(12, 25000, 750000)
    else:
        GPIO.output(6,0)#Speed 100% Duty Cycle and default if out of range 0-4
        pi.hardware_PWM(12, 25000, 1000000)

    if humidifierIntensity == 0 :#No Humidity
        GPIO.output(13,1)
        GPIO.output(19,1)
        GPIO.output(26,1)
    elif humidifierIntensity == 1 :#One Humidifier On
        GPIO.output(13,0)
        GPIO.output(19,1)
        GPIO.output(26,1)
    elif humidifierIntensity == 2 :#Two Humidifiers On
        GPIO.output(13,0)
        GPIO.output(19,0)
        GPIO.output(26,1)
    else:#All three Humidifiers On
        GPIO.output(13,0)
        GPIO.output(19,0)
        GPIO.output(26,0)

    return


def auto_control(currentTemp, tempSetting, currentHumidity, humidityCap):

    tempDifference = int(currentTemp) - int(tempSetting)
    print('tempDifference:', tempDifference)
    if tempDifference < 0:  # lower fanSpeed since your current temp is lower than your set temp
        fanSpeed = 0
    elif tempDifference == 0:  # Do nothing, the current settings are working
        pass
    elif tempDifference in tempRange_1:
        if fanSpeed <= 1:  # Do nothing, you're close to set temp
            pass
        else:
            fanSpeed = fanSpeed - 1  # Lower fanspeed since you're getting close
    elif tempDifference in tempRange_2:
        if fanSpeed <= 2:
            fanSpeed = fanSpeed + 1  # Raise fanspeed to get closer to set temp
        else:  # do nothing since you're on your way to set temp
            pass
    elif tempDifference in tempRange_3:
        if fanSpeed <= 2:
            fanSpeed = fanSpeed + 1  # Raise fanspeed to get closer to set temp
        else:  # do nothing since you're on your way to set temp
            pass
    elif tempDifference in tempRange_4:
        if fanSpeed <= 3:
            fanSpeed = fanSpeed + 1  # Raise fanspeed to get closer to set temp
        else:  # do nothing since you're on your way to set temp
            pass
    else:
        fanSpeed = 4  # max fan speed

    humidityDifference = int(humidityCap) - int(currentHumidity)
    print("humidityDifference:", humidityDifference)
    if humidityDifference < 0:  # turn off humidifiers since it's too humid
        humidifierIntensity = 0
    elif humidityDifference == 0:  # Do nothing, the current settings are working
        pass
    elif humidityDifference in humidityRange_1:
        if humidifierIntensity <= 1:  # Do nothing, you're close to set humidity
            pass
        else:
            humidifierIntensity = humidifierIntensity - 1  # Lower humidifierIntensity since you're getting close
    elif humidityDifference in humidityRange_2:
        if humidifierIntensity <= 1:
            humidifierIntensity = humidifierIntensity + 1  # Raise humidifierIntensity to get closer to set humidity cap
        else:  # do nothing since you're on your way to set humidity cap
            pass
    elif humidityDifference in humidityRange_3:
        if humidifierIntensity <= 2:
            humidifierIntensity = humidifierIntensity + 1  # Raise humidifierIntensity to get closer to set humidity cap
        else:  # do nothing since you're on your way to set humidity cap
            pass
    else:
        humidifierIntensity = 3  # max humidifierIntensity
    
    return



# try:
#     while True:
#         print("Currently Using Dummy Variables:")
#         AutoMode = int(input("Input AutoMode(0/1): "))  # set AutoMode
#         print("AutoMode = ", AutoMode)
# 
#         if AutoMode >= 1:
#             # AutoMode code
#             print("Auto Mode Selected:")
#             currentTemp = input("Input current temperature(0-50 Celcius): ")  # sense current temperature (currentTemp)
#             tempSetting = input("Input temp. setting 20-32 Celcius (68-90 F):")  # set temperature (tempSetting)
#             currentHumidity = input("Input current humidity(0-100%): ")  # sense current humidity (currentHumidity)
#             humidityCap = input("Input humidity cap setting(0-100%): ")  # set humidity percentage (humidityCap)
#             auto_control(currentTemp, tempSetting, currentHumidity, humidityCap)
# 
#         else:
#             print("Manual Mode Selected:")
#             fanSpeed = int(input("Input Fan Speed(0-4): "))  # set fanSpeed
#             humidifierIntensity = int(input("Input Humidifier Intensity(0-3): "))  # set humidifierIntensity
#             manual_control(fanSpeed, humidifierIntensity)
# 

#
# try:
#     while True:
#         Fanspeed = int(input("Fan Speed: "))
#         manual_control(Fanspeed, 0)
#         
# except KeyboardInterrupt:
#     print("Press Ctrl-C to terminate while loop:")
#     GPIO.output(6, 1)
#     GPIO.output(13, 1)
#     GPIO.output(19, 1)
#     GPIO.output(26, 1)
#     manual_control(0,0)
#     pass
