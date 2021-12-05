import minimalmodbus
import serial
import sys, os, io
import time 

debug = False
run = True
sleepTime = 5
#devName = '/dev/ttyUSB0' #USB Connection
devName = '/dev/serial0' #TX RX Serial connection (pin 8 &  10)

#debug mode to see if data is polled correctly
if (len(sys.argv) > 1):
        if (sys.argv[1] == "-d"):
                debug=True
                sleepTime = 2
                print("sys.argv[0]: Debug: enabled")

renogy = minimalmodbus.Instrument(devName, 1)
renogy.serial.baudrate = 9600
renogy.serial.bytesize = 8
renogy.serial.parity   = serial.PARITY_NONE
renogy.serial.stopbits = 1
renogy.serial.timeout = 2
renogy.debug = debug

lowPower = False

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

if (debug): print(minimalmodbus._get_diagnostic_string())

if (debug):
        # Print the details of the power meter here, also include the config needed to talk to the unit.
        print('Details of the serial connection:')
        print("Renogy:", renogy)

def readRenogy(fileObj):
        try:
                if (run):
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

                #for production
                if (run): print("Battery SOC:", float(charge_level), "%")
                valName  = "mode=\"SOC\""
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {float(register)}"
                print(dataStr, file=fileObj)
                
                #for testing
                batVolts = renogy.read_register(0x101)
                #batVolts = 127
                batVolts = batVolts/10
                if (run): print("Battery Voltage:", float(batVolts), "v")
                valName  = "mode=\"batVolts\""
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {batVolts}"
                print(dataStr, file=fileObj)
                
                #for production
                charging_amps = renogy.read_register(0x102)
                charging_amps = float(charging_amps/100)
                if (run): print("Charging Amps:", charging_amps, "a")


                #for testing
                register = renogy.read_register(0x107)
                if (run): print("PV volts:", float(register/10), "v")
                valName  = "mode=\"pvVolts\""
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {float(register/10)}"
                print(dataStr, file=fileObj)
                
                #for production
                panel_current = renogy.read_register(0x108)
                panel_current = float(panel_current/100)
                if (run): print("PV Amps:", panel_current, "a")
                valName  = "mode=\"pvAmps\""
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {float(register/100)}"
                print(dataStr, file=fileObj)
                
                #for production
                pvWatts = renogy.read_register(0x109)
                if (run): print("PV watts:", pvWatts, "w")
                valName  = "mode=\"pvWatts\""
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {pvWatts}"
                print(dataStr, file=fileObj)
                
                #for testing
                register = renogy.read_register(0x120)
                chargeStateNum = register & 0x00ff
                chargeStateStr = CHARGING_STATE.get(chargeStateNum)
                if (run): print("Charge state:", chargeStateNum, chargeStateStr)
                valName  = "mode=\"chargeState\""
                valName  = "{" + valName + ", myStr=\"" + chargeStateStr + "\"}"
                dataStr  = f"Renogy{valName} {chargeStateNum}"
                print(dataStr, file=fileObj)

                #for testing
                register = renogy.read_register(0xE004)
                batTypeStr = BATTERY_TYPE.get(register)
                if (run): print("Bat Type:", batTypeStr)
                valName  = "mode=\"batType\""
                valName  = "{" + valName + ", myStr=\"" + batTypeStr + "\"}"
                dataStr  = f"Renogy{valName} {register}"
                print(dataStr, file=fileObj)
                
                return [batVolts, charging_amps, panel_current, pvWatts, charge_level] 

        except IOError:
                print("Failed to read from instrument")

# Run the function to read the power meter.
# 
# while True:
#         if (debug): print("Opened new tmp file /ramdisk/Renogy.prom.tmp")
#         file_object = open('/ramdisk/Renogy.prom.tmp', mode='w')
# 
#         # write data here
# 
#         if (debug): print("\nReading Renogy Wanderer data...")
#         Bat_Volt = readRenogy(file_object)
#         print('TESTING Bat Volts!')
#         print(str(Bat_Volt))
# 
#         file_object.flush()
#         file_object.close()
#         outLine = os.system('/bin/mv /ramdisk/Renogy.prom.tmp /ramdisk/Renogy.prom')
# 
#         time.sleep(sleepTime)

def get_power_data():
    # return [batVolts, charging_amps, panel_current, pvWatts] 

    if (debug): print("Opened new tmp file /ramdisk/Renogy.prom.tmp")
    file_object = open('/ramdisk/Renogy.prom.tmp', mode='w')

        # write data here

    if (debug): print("\nReading Renogy Wanderer data...")
        
    power_metrics = readRenogy(file_object)
    print('TESTING Bat Volts!')
    print(power_metrics)

    file_object.flush()
    file_object.close()
    outLine = os.system('/bin/mv /ramdisk/Renogy.prom.tmp /ramdisk/Renogy.prom')
    
    return power_metrics
