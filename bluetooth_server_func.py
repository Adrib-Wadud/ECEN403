from bluetooth import *
from cooling_subsystem_refined import manual_control, auto_control
from renogywanderer import get_power_data
from MCP3008 import MCP3008
from LCD import LCD

def blu_server(FS, HI, power_data, TS, HS, p_list, C_L, B_V, B_A, P_A, P_W):
    fan_speed = 0
    humidity_intensity = HI.value
    humidity_intensity = int(humidity_intensity)
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]
    uuid = "163660a6-ad17-44fc-99c5-5c75e78ad815"

    advertise_service( server_sock, "SampleServer",
                       service_id = uuid,
                       service_classes = [ uuid, SERIAL_PORT_CLASS ],
                       profiles = [ SERIAL_PORT_PROFILE ],
    #                   protocols = [ OBEX_UUID ]
                        )

    #print("Waiting for connection on RFCOMM channel %d" % port)

    #client_sock, client_info = server_sock.accept()
    client_sock = None
    #print("Accepted connection from ", client_info)
    curr_temperature = 72
    curr_humidity = 20
    set_temperature = TS.value
    set_humidity = HS.value
    #fan_speed = 0
    #humidity_intensity = 0
    charge_level = 100
    fan_speed_map = {0: 0, 25: 1, 50: 2, 75: 3, 100:4}
    f_map = {0:0, 1:25, 2:50, 3:75, 4:100}
    adc = MCP3008()
    
    try:
        while True:
            if client_sock is None:
                print("Waiting for connection on RFCOMM channel %d" % port)
                client_sock, client_info = server_sock.accept()
                print("Accepted connection from ", client_info)
            curr_temperature = round(adc.getTemperature(0))
            curr_humidity = round(adc.getHumidity(1))
            print(FS.value)
            try:
                data = client_sock.recv(1024)
            except:
                client_sock = None
                pass
                continue
            
            print(data)
            data = data.decode('utf-8')
            print(data)
            if len(data) == 0: break
            if data == 'Activate Auto Mode!\n':
                client_sock.send('Auto mode activation command recieved')
                auto_control(curr_temperature, set_temperature, curr_humidity, set_humidity)
            elif data == 'Activate Manual Mode!\n':
                client_sock.send('Manual mode activation command received')
            elif data == 'Temperature Up!\n':
                if set_temperature <90:
                    set_temperature = set_temperature + 1
                    TS.value +=1
                    auto_control(curr_temperature, TS.value, curr_humidity, HS.value)
                    client_sock.send('Temperature up command received')
                elif set_temperature == 90:
                    client_sock.send('Temperature cannot go above 90 F')
            elif data == 'Temperature Down!\n':
                if set_temperature > 40:
                    set_temperature = set_temperature - 1
                    TS.value -= 1
                    auto_control(curr_temperature, TS.value, curr_humidity, HS.value)
                    client_sock.send('Temperature down command received')
                elif set_temperature == 40:
                    client_sock.send('Temperature cannot go below 40 F')
            elif data == 'Humidity Up!\n':
                if set_humidity < 100:
                    set_humidity = set_humidity + 1
                    HS.value += 1
                    auto_control(curr_temperature, TS.value, curr_humidity, HS.value)
                    client_sock.send('Humidity up command received')
                elif set_humidity == 100:
                    client_sock.send('Humidity cannot go above 100 %')
            elif data == 'Humidity Down!\n':
                if set_humidity > 0:
                    set_humidity = set_humidity - 1
                    HS.value -= 1
                    auto_control(curr_temperature, TS.value, curr_humidity, HS.value)
                    client_sock.send('Humidty down command received')
                elif set_humidity == 0:
                    client_sock.send('Humidity cannot go below 0 %')
            elif data == 'Fan Speed Up!\n':
                if FS.value < 4:
                    fan_speed = fan_speed + 1
                    FS.value = FS.value + 1
                    client_sock.send('Fan speed up command received')
                    print(FS.value)
                    #print('Blu :' + str(fan_speed_map[FS.value]))
                    #manual_control(FS.value, phy.humidifierIntensity)
                    manual_control(FS.value, HI.value)
                elif FS.value == 4:
                    client_sock.send('Max Fan speed reached')
            elif data == 'Fan Speed Down!\n':
                if FS.value > 0 :
                    fan_speed = fan_speed - 1
                    FS.value = FS.value -1
                    client_sock.send('Fan speed down command received')
                    print(FS.value)
                    #print('Blu :' + str(fan_speed_map[FS.value]))
                    #manual_control(FS.value, phy.humidifierIntensity)
                    manual_control(FS.value, HI.value)
                elif FS.value == 0:
                    client_sock.send('Fan OFF')
            elif data == 'Humidifier Intensity Up!\n':
                if HI.value < 3:
                    humidity_intensity = humidity_intensity + 1
                    HI.value = HI.value + 1
                    client_sock.send('Humidifier intensity up command received')
                    #manual_control(phy.fanSpeed,humidity_intensity)
                    manual_control(FS.value, HI.value)
                elif HI.value == 3:
                    client_sock.send('Max humidifier intensity reached')
            elif data == 'Humidifier Intensity Down!\n':
                if HI.value > 0:
                    humidity_intensity = humidity_intensity - 1
                    HI.value = HI.value - 1
                    client_sock.send('Humidifier intensity down command received')
                    manual_control(FS.value, HI.value)
                    #manual_control(fan_speed,humidity_intensity)
                elif HI.value == 0:
                    client_sock.send('Humidifier OFF')
            elif data == 'Deactivate Manual Mode!\n':
                client_sock.send('Manual Mode deactivation command received')
            elif data == 'Deactivate Auto Mode!\n':
                client_sock.send('Auto mode deactivation command received')
            elif data == 'Get current temperature!\n':
                msg = str(curr_temperature) + ' F'
                print(msg)
                client_sock.send(msg)
            elif data == 'Get current humidity!\n':
                msg = str(curr_humidity) + ' %'
                client_sock.send(msg)
            elif data == 'Get set temperature!\n':
                msg = str(TS.value) + ' F'
                client_sock.send(msg)
            elif data == 'Get set humidity!\n':
                msg = str(HS.value) + ' %'
                client_sock.send(msg)
            elif data == 'Get current fan speed!\n':
                msg = f_map[FS.value]
                msg = str(msg)
                client_sock.send(msg)
            elif data == 'Get current humidity intensity!\n':
                msg = str(HI.value)
                client_sock.send(msg)
            elif data == 'Get current charge!\n':
                #charge_level = power_data.batteryLevel
                #print('Battery level: ' + str(power_data.batteryLevel))
                #charge_level = p_list[4]
                charge_level = C_L.value
                print(charge_level)
                client_sock.send(str(charge_level))

            elif data == 'Get current bat_volt!\n':
                #bat_volt = power_data.batteryVoltage
                bat_volt = B_V.value
                client_sock.send(str(bat_volt))
                    
#                     bat_volt = default_power[0]
#                     charge_amps = default_power[1]
#                     pan_watts = default_power[2]
#                     pan_amps = default_power[3]
#                     print(bat_volt)
#                     msg = str(bat_volt)
#                     print(msg)
#                     client_sock.send(msg)
                        
            elif data == 'Get current charge_amps!\n':
                #charge_amps = power_data.batteryAmperage
                charge_amps = B_A.value
                client_sock.send(str(charge_amps))
            elif data == 'Get current pan_watts!\n':
                #pan_watts = power_data.panelWattage
                pan_watts = P_W.value
                client_sock.send(str(pan_watts))
            elif data == 'Get current pan_amps!\n':
                #pan_amps = power_data.panelAmperage
                pan_amps = P_A.value
                client_sock.send(str(pan_amps))
                


    except KeyboardInterrupt:
        print("Press Ctrl-C to terminate while loop:")
        GPIO.output(6, 1)
        GPIO.output(13, 1)
        GPIO.output(19, 1)
        GPIO.output(26, 1)
        manual_control(0,0)
        pass
    print("disconnected")

    client_sock.close()
    server_sock.close()
    print("all done")
