#This file is used to test the GPIO pins of the raspberry pi
import RPi.GPIO as GPIO
import time

GPIO_PIN = 24

GPIO.setmode(GPIO.BOARD) #use physical pin numbers to refer to GPIO pins
GPIO.setwarnings(False) #disable warnings

GPIO.setup(GPIO_PIN, GPIO.OUT) #set pin as an output

print("Turning LED on")
GPIO.output(GPIO_PIN, GPIO.HIGH) #set pin HIGH
time.sleep(1) #delay 1 second
print("Turning LED off")
GPIO.output(GPIO_PIN, GPIO.LOW) #set pin LOW
