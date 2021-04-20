from MCP3008 import MCP3008
from time import time
from sys import exit

SENSOR_UPDATE_TIME = 1 #seconds

#initialize ADC
adc = MCP3008()

#defining variables for use in main program loop
temperatureChannel = 0 #ADC channel connected to temp sensor
temperatureSum = 0 #running sum of temp sensor readings (averaged to smooth sensor output)

humidityChannel = 1 #ADC channel connected to humidity sensor
humiditySum = 0 #running sum of humidity sensor readings (averaged to smooth sensor output)

numReadings = 0 #count of readings (used when averaging sensor voltage output)
pastSensorTime = time() #save time to allow sensor reading averages to be output every second

while True: #sensor reading display loop
    try:
        #counting each temperature and humidity reading and adding to individual sums in preparation for averaging
        currentTemperature = adc.getTemperature(temperatureChannel)
        temperatureSum += currentTemperature
        currentHumidity = adc.getHumidity(humidityChannel, currentTemperature)
        humiditySum += currentHumidity
        numReadings += 1
        
        presentTime = time()
        if((presentTime - pastSensorTime) >= SENSOR_UPDATE_TIME): #after every second, calculate sensor data averages
            #average temperature and humidity readings and round to one decimal place
            temperature = round(temperatureSum / numReadings, 1)
            print("Temperature:", temperature, u"\N{DEGREE SIGN}C")
            humidity = round(humiditySum / numReadings, 1)
            print("Humidity:", humidity)
            
            #reset variables used for 1 second averaging
            temperatureSum, humiditySum, numReadings = 0, 0, 0
            pastSensorTime = presentTime
    
    except KeyboardInterrupt:
        sys.exit("Program Terminated")