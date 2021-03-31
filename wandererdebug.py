#!/usr/bin/env python3

# pip3 uninstall pyserial
# pip3 uninstall serial
# pip3 uninstall minimalmodbus
# pip3 install pyserial
# pip3 install minimalmodbus

import minimalmodbus
import serial
import sys, os, io
import time 

debug = True
sleepTime = 10
devName = '/dev/ttyUSB0'

if (len(sys.argv) > 1):
        if (sys.argv[1] == "-d"):
                debug=True
                sleepTime = 2
                print("sys.argv[0]: Debug: enabled")

#serial communication info
renogy = minimalmodbus.Instrument(devName, 1)
renogy.serial.baudrate = 9600
renogy.serial.bytesize = 8
renogy.serial.parity   = serial.PARITY_NONE
renogy.serial.stopbits = 1
renogy.serial.timeout = 2
renogy.debug = debug

BATTERY_TYPE = {
    1: 'open',
    2: 'sealed',
    3: 'gel',
    4: 'lithium',
    5: 'self-customized'
}

CHARGING_STATE = {
    0: 'deactivated',
    1: 'activated',
    2: 'mppt',
    3: 'equalizing',
    4: 'boost',
    5: 'floating',
    6: 'current limiting'
}

if (debug): print(minimalmodbus._get_diagnostic_string()) #print diagnostic info

if (debug):
        # Print config to talk to unit and serial connection.
        print('Details of the serial connection:')
        print("Renogy:", renogy)

def readContr(fileObj): #function to read data
        try:
                if (debug): #conditional for debug mode
		
		#read battery SOC
                register = renogy.read_register(0x100)#0x100 has actual value
                if (debug): print("Battery SOC:", float(register), "%")#print to terminal
		
		#format for writing data to file
                valName  = "mode=\"SOC\""
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {float(register)}"
                print(dataStr, file=fileObj)
		
		#read battery voltage
                batVolts = renogy.read_register(0x101) #0x100 has 10*actual value
                batVolts = batVolts/10
                if (debug): print("Battery Voltage:", float(batVolts), "v") #print to terminal

                #format for writing data to file
                valName  = "mode=\"batVolts\""
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {batVolts}"
                print(dataStr, file=fileObj)
               
        except IOError:
                print("Failed to read from controller")

#temp file block

while True:
        if (debug): print("Opened new temp file /test403/Renogy.prom.tmp")
        #create a new file to write into
        file_object = open('/test403/Renogy.prom.tmp', mode='w')

        #write data with readContr
        if (debug): print("\nReading Charge Controller data...")
        readContr(file_object)
        
        #flush internal buffer and close file
        file_object.flush()
        file_object.close()
        
        outLine = os.system('/bin/mv /test403/Renogy.prom.tmp /test403/Renogy.prom')

        time.sleep(sleepTime)
