from spidev import SpiDev


class MCP3008:
    VREF = 5

    def __init__(self, bus=0, device=0):
        self.bus, self.device = bus, device
        # Initializing and characterizing SPI bus
        self.spi = SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 3900000  # 3.9MHz (MCP3008 supports up to 4.8MHz - 200ksps @ 24 clk pulses/sample)

    def getVoltage(self, channel):  # reads voltage from specified channel
        rawData = self.spi.xfer([1, (8 + channel) << 4, 0])
        processedData = ((rawData[1] & 3) << 8) + rawData[2]
        voltage = (processedData / 1024) * self.VREF

        return voltage

    def getTemperature(self, channel):  # reads volage and converts to rounded temperature value
        temperatureVoltage = self.getVoltage(channel)
        temperature = temperatureVoltage / 0.010  # 10mV/C (from LM35 datasheet)
        # temperature = 25 + (temperatureVoltage - 0.750) / 0.010 #10mV/C (from TMP36 datasheet)

        return temperature

    def getHumidity(self, channel, temperature):  # reads volage and converts to rounded humidity value
        humidityVoltage = self.getVoltage(channel)
        sensorHumidity = ((humidityVoltage / self.VREF) - 0.16) / 0.0062  # sensor voltage to humidity conversion (from HIH-4000 datasheet)
        humidity = sensorHumidity / (1.0546 - 0.00216 * temperature)  # adjusting humidity reading for temperature dependency
        # (from HIH-4000 datasheet)
        return humidity

    def close(self):
        self.spi.close()