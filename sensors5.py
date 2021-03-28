from MCP3008 import MCP3008
from time import time

mcp = MCP3008()

#defining variables for use in main program loop
tempChannel = 0 #ADC channel connected to temp sensor
tempVoltageSum = 0 #running sum of temp sensor voltage readings (averaged to smooth sensor voltage output)
numReadings = 0 #count of readings (used when averaging sensor voltage output)
pastTime = time() #save time to allow sensor reading averages to be output every second

while True: #sensor reading display loop
    #counting each voltage reading and adding to sum in preparation for averaging
    tempVoltage = mcp.getVoltage(tempChannel)
    tempVoltageSum += tempVoltage
    numReadings += 1
    
    presentTime = time()
    if((presentTime - pastTime) >= 1): #after every second, average sensor voltage output and convert to sensor reading
        averageTempVoltage = tempVoltageSum / numReadings
        temperature = mcp.convertToTemp(averageTempVoltage)
        print("Temperature:", temperature, u"\N{DEGREE SIGN}C")
        
        #reset variables used for 1 second averaging
        tempVoltageSum, numReadings = 0, 0
        pastTime = presentTime