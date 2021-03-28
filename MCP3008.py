from spidev import SpiDev
 
class MCP3008:
    
    VREF = 5
    
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        #Initializing and characterizing SPI bus
        self.spi = SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 3900000 # 3.9MHz (MCP3008 supports up to 4.8MHz - 200ksps @ 24 clk pulses/sample)
    
    def getVoltage(self, channel): #reads voltage from specified channel
        rawData = self.spi.xfer([1, (8 + channel) << 4, 0])
        processedData = ((rawData[1]&3) << 8) + rawData[2]
        voltage = (processedData / 1024) * self.VREF
        return voltage

    def convertToTemp(self, voltage, decimalPlaces = 2): #converts voltage to rounded temperature value
        temperature = voltage / 0.010 #10mV/C (from LM35 temp sensor datasheet)
        temperature = round(temperature, decimalPlaces)
        return temperature
            
    def close(self):
        self.spi.close()