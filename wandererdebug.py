
import minimalmodbus
import serial
import sys, os, io
import time 

debug = False
run = True
sleepTime = 10
devName = '/dev/ttyUSB0'

#if statement to enable debug mode
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

lowPower = False

#battery types
BATTERY_TYPE = {
    1: 'open',
    2: 'sealed',
    3: 'gel',
    4: 'lithium',
    5: 'self-customized'
}

#charging states
CHARGING_STATE = {
    0: 'deactivated',
    1: 'activated',
    2: 'mppt',
    3: 'equalizing',
    4: 'boost',
    5: 'floating',
    6: 'current limiting'
}

#print diagnostic info
if (debug): print(minimalmodbus._get_diagnostic_string())

if (debug):
         # Print config to talk to unit and serial connection.
        print('Details of the serial connection:')
        print("Renogy:", renogy)

def readRenogy(fileObj): #function to read data
        try:
                if (run): #run the code

                #dummy variable for battery SOC
                #register = 25
                fanspeed = 4
                humidIntensity = 4
                lowPower == False
                maxFanspeed = 4
                maxHIntensity = 4
                
                print("Currently Using Dummy Variables:")
                print("Max Fan Speed:", maxFanspeed)
                print("Max Humidifier Intensity:", maxHIntensity)
                fanspeed = int(input("Input Fan Speed(0/4): "))
                humidIntensity = int(input("Input Humidity Intensity Level (0/4): "))
                
                #battery SOC
                register = renogy.read_register(0x100)#read register and print to terminal
                print("Fan Speed:", float(fanspeed))
                print("Humidifier Intensity:", float(humidIntensity))

                
                if (run): print("Battery SOC:", float(register), "%")
                valName  = "mode=\"SOC\"" #format for writing data to file
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {float(register)}"
                print(dataStr, file=fileObj) #print to temp file
                #low power block
                if(register == 100):
                    print("Able to reach maximum fan speed and humidifier")
                
                if(register == 75):
                    print("Still able to reach maximum fan speed and humidifier")
                         
                if(register == 25):#low power mode block
                    print("Entering Low Power Mode... capping fan speed and humidifier intensity to 1!")
                    maxFanspeed =1
                    maxHIntensity = 1
                    print("Max Fan Speed:", maxFanspeed)
                    print("Max Humidifier Intensity:", maxHIntensity)
                    if (fanspeed >1):
                         fanspeed = 1
                         print("Fan Speed:", float(fanspeed))
                    else:
                         print("Fan Speed:", float(fanspeed))
                    if (humidIntensity >1):
                         humidIntensity =1
                         print("Humidifier Intensity:", float(humidIntensity))
                    else:
                         print("Humidifier Intensity:", float(humidIntensity))
                if(register == 0):
                    print("Turning off fan and humidifier! Charge battery!")
                    MAXFanspeed =0
                    MAXHIntensity = 0
                    if(fanspeed >0):
                         fanspeed = 0
                    if(humidIntensity >0):
                         humidIntensity =0

                batVolts = renogy.read_register(0x101)#battery voltage block
                #batVolts = 127
                batVolts = batVolts/10
                if (run): print("Battery Voltage:", float(batVolts), "v")
                valName  = "mode=\"batVolts\"" #format for writing data to file
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {batVolts}"
                print(dataStr, file=fileObj)

                register = renogy.read_register(0x102)#battery charging amps
                if (run): print("Charging Amps:", float(register/100), "a")

                register = renogy.read_register(0x107)#PV VOltage
                if (run): print("PV volts:", float(register/10), "v") #read register
                valName  = "mode=\"pvVolts\"" #format for writing data to file
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {float(register/10)}"
                print(dataStr, file=fileObj)

                register = renogy.read_register(0x108)#PV Amps
                if (run): print("PV amps:", float(register/100), "a")#read register
                valName  = "mode=\"pvAmps\"" #format for writing data to file
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {float(register/100)}"
                print(dataStr, file=fileObj)

                pvWatts = renogy.read_register(0x109)#PV Watts
                if (run): print("PV watts:", pvWatts, "w")
                valName  = "mode=\"pvWatts\"" #format for writing data to file
                valName  = "{" + valName + "}"
                dataStr  = f"Renogy{valName} {pvWatts}"
                print(dataStr, file=fileObj)
                
                register = renogy.read_register(0x120)#Charging state
                chargeStateNum = register & 0x00ff
                chargeStateStr = CHARGING_STATE.get(chargeStateNum)
                if (run): print("Charge state:", chargeStateNum, chargeStateStr)#read register
                valName  = "mode=\"chargeState\"" #format for writing data to file
                valName  = "{" + valName + ", myStr=\"" + chargeStateStr + "\"}"
                dataStr  = f"Renogy{valName} {chargeStateNum}"
                print(dataStr, file=fileObj)


                register = renogy.read_register(0xE004)#Battery Type
                batTypeStr = BATTERY_TYPE.get(register)
                if (run): print("Bat Type:", batTypeStr)#read register
                valName  = "mode=\"batType\"" #format for writing data to file
                valName  = "{" + valName + ", myStr=\"" + batTypeStr + "\"}"
                dataStr  = f"Renogy{valName} {register}"
                print(dataStr, file=fileObj)

        except IOError:
                print("Failed to read from instrument")

# Run the function to read the power meter.
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
