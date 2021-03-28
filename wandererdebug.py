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

debug = True #enable debug mode
sleepTime = 10
devName = '/dev/ttyUSB0' #USB port utilized

if (len(sys.argv) > 1):
        if (sys.argv[1] == "-d"):
                debug=True
                sleepTime = 2
                print("sys.argv[0]: Debug: enabled")
                
#serial connection information
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
       
        print('Details of the serial connection:')
        print("Renogy:", renogy)

def readRenogy(fileObj):
        try:
                if (debug):
                        register = renogy.read_register(0x00A)
                        maxV = register >> 8
                        maxC = register & 0x00ff
                        if (debug): print("Max sys voltage:", float(maxV), "v")
                        if (debug): print("Max sys amps:", float(maxC), "a")

                        register = renogy.read_register(0x00B)
                        maxD = register >> 8
                        prodType = register & 0x00ff
                        if (debug): print("max discharge:", float(maxD), "a")
                        if (debug): print("sys type:", prodType, "00=controller 1=inverter")

                register = renogy.read_register(0x100)
                if (debug): print("Battery SOC:", float(register), "%")
                valName  = "mode=\"SOC\""
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {float(register)}"
                print(dataStr, file=fileObj)

                batVolts = renogy.read_register(0x101)
                batVolts = batVolts/10
                if (debug): print("Battery Voltage:", float(batVolts), "v")
                valName  = "mode=\"batVolts\""
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {batVolts}"
                print(dataStr, file=fileObj)

                register = renogy.read_register(0x102)
                if (debug): print("Charging Amps:", float(register/100), "a")

                register = renogy.read_register(0x103)
                controller_temp_bits = register >> 8
                temp_value = controller_temp_bits & 0x0ff
                sign = controller_temp_bits >> 7
                devTemp = -(temp_value - 128) if sign == 1 else temp_value
                if (debug): print("controller temp:", float(devTemp), "C")
                valName  = "mode=\"sccTemp\""
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {float(devTemp)}"
                print(dataStr, file=fileObj)


                register = renogy.read_register(0x107)
                if (debug): print("PV volts:", float(register/10), "v")
                valName  = "mode=\"pvVolts\""
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {float(register/10)}"
                print(dataStr, file=fileObj)

                register = renogy.read_register(0x108)
                if (debug): print("PV amps:", float(register/100), "a")
                valName  = "mode=\"pvAmps\""
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {float(register/100)}"
                print(dataStr, file=fileObj)

                pvWatts = renogy.read_register(0x109)
                if (debug): print("PV watts:", pvWatts, "w")
                valName  = "mode=\"pvWatts\""
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {pvWatts}"
                print(dataStr, file=fileObj)


                register = renogy.read_register(0x120)
                chargeStateNum = register & 0x00ff
                chargeStateStr = CHARGING_STATE.get(chargeStateNum)
                if (debug): print("Charge state:", chargeStateNum, chargeStateStr)
                valName  = "mode=\"chargeState\""
                valName  = "{" + valName + ", myStr=\"" + chargeStateStr + "\"}"
                dataStr  = f"Renogy{valName} {chargeStateNum}"
                print(dataStr, file=fileObj)


                register = renogy.read_register(0xE004)
                batTypeStr = BATTERY_TYPE.get(register)
                if (debug): print("Bat Type:", batTypeStr)
                valName  = "mode=\"batType\""
                valName  = "{" + valName + ", myStr=\"" + batTypeStr + "\"}"
                dataStr  = f"Renogy{valName} {register}"
                print(dataStr, file=fileObj)

                return

        except IOError:
                print("Failed to read from instrument")
                #I/O error

while True:
        if (debug): print("Opened new tmp file /ramdisk/Renogy.prom.tmp")
        file_object = open('/ramdisk/Renogy.prom.tmp', mode='w')

        # write data here

        if (debug): print("\nReading Renogy Wanderer data...")
        readRenogy(file_object)

        file_object.flush()
        file_object.close()
        outLine = os.system('/bin/mv /ramdisk/Renogy.prom.tmp /ramdisk/Renogy.prom')

        time.sleep(sleepTime)
