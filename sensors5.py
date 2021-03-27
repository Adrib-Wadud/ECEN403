import spidev
import time

VREF = 5

def getVoltage(channel): #reads voltage from specified channel
    rawData = spi.xfer([1, (8 + channel) << 4, 0])
    processedData = ((rawData[1]&3) << 8) + rawData[2]
    voltage = (processedData / 1024) * VREF
    return voltage

def convertToTemp(voltage, decimalPlaces = 2): #converts voltage to rounded temperature value
    temperature = voltage / 0.010 #10mV/C (from LM35 temp sensor datasheet)
    temperature = round(temperature, decimalPlaces)
    return temperature

#Initializing and characterizing SPI bus
bus = 0
device = 0
spi = spidev.SpiDev()
spi.open(bus, device)
spi.max_speed_hz = 3900000 #3.9MHz (ADC supports up to 4.8MHz - 200ksps @ 24 clk pulses/sample)

#defining variables for use in main program loop
tempChannel = 0 #ADC channel connected to temp sensor
tempVoltageSum = 0 #running sum of temp sensor voltage readings (averaged to smooth sensor voltage output)
numReadings = 0 #count of readings (used when averaging sensor voltage output)
pastTime = time.time() #save time to allow sensor reading averages to be output every second

while True: #sensor reading display loop
    #counting each voltage reading and adding to sum in preparation for averaging
    tempVoltage = getVoltage(tempChannel)
    tempVoltageSum += tempVoltage
    numReadings += 1
    
    presentTime = time.time()
    if((presentTime - pastTime) >= 1): #after every second, average sensor voltage output and convert to sensor reading
        averageTempVoltage = tempVoltageSum / numReadings
        temperature = convertToTemp(averageTempVoltage)
        print("Temperature: ", temperature)
        
        #reset variables used for 1 second averaging
        tempVoltageSum, numReadings = 0, 0
        pastTime = presentTime
    
