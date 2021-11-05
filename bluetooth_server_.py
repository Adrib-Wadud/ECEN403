from bluetooth import *
from cooling_subsystem_refined import manual_control, auto_control
# from renogywanderer import get_power_data


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

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)
curr_temperature = 72
curr_humidity = 20
set_temperature = 87
set_humidity = 90
fan_speed = 0
humidity_intensity = 0
charge_level = 100
 
try:
    while True:
        data = client_sock.recv(1024)
        print(data)
        data = data.decode('utf-8')
        print(data)
        if len(data) == 0: break
        if data == 'Activate Auto Mode!\n':
            client_sock.send('Auto mode activation command recieved')
        elif data == 'Activate Manual Mode!\n':
            client_sock.send('Manual mode activation command received')
        elif data == 'Temperature Up!\n':
            if set_temperature <90:
                set_temperature = set_temperature + 1
                client_sock.send('Temperature up command received')
            elif set_temperature == 90:
                client_sock.send('Temperature cannot go above 90 F')
        elif data == 'Temperature Down!\n':
            if set_temperature > 40:
                set_temperature = set_temperature - 1
                client_sock.send('Temperature down command received')
            elif set_temperature == 40:
                client_sock.send('Temperature cannot go below 40 F')
        elif data == 'Humidity Up!\n':
            if set_humidity < 100:
                set_humidity = set_humidity + 5
                client_sock.send('Humidity up command received')
            elif set_humidity == 100:
                client_sock.send('Humidity cannot go above 100 %')
        elif data == 'Humidity Down!\n':
            if set_humidity > 0:
                set_humidity = set_humidity - 5
                client_sock.send('Humidty down command received')
            elif set_humidity == 0:
                client_sock.send('Humidity cannot go below 0 %')
        elif data == 'Fan Speed Up!\n':
            if fan_speed < 4:
                fan_speed = fan_speed + 1
                client_sock.send('Fan speed up command received')
                manual_control(fan_speed,humidity_intensity)
            elif fan_speed == 4:
                client_sock.send('Max Fan speed reached')
        elif data == 'Fan Speed Down!\n':
            if fan_speed > 0 :
                fan_speed = fan_speed - 1
                client_sock.send('Fan speed down command received')
                manual_control(fan_speed,humidity_intensity)
            elif fan_speed == 0:
                client_sock.send('Fan OFF')
        elif data == 'Humidifier Intensity Up!\n':
            if humidity_intensity < 3:
                humidity_intensity = humidity_intensity + 1
                client_sock.send('Humidifier intensity up command received')
                manual_control(fan_speed,humidity_intensity)
            elif humidity_intensity == 3:
                client_sock.send('Max humidifier intensity reached')
        elif data == 'Humidifier Intensity Down!\n':
            if humidity_intensity > 0:
                humidity_intensity = humidity_intensity - 1
                client_sock.send('Humidifier intensity down command received')
                manual_control(fan_speed,humidity_intensity)
            elif humidity_intensity == 0:
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
            msg = str(set_temperature) + ' F'
            client_sock.send(msg)
        elif data == 'Get set humidity!\n':
            msg = str(set_humidity) + ' %'
            client_sock.send(msg)
        elif data == 'Get current fan speed!\n':
            msg = str(fan_speed)
            client_sock.send(msg)
        elif data == 'Get current humidity intensity!\n':
            msg = str(humidity_intensity)
            client_sock.send(msg)
        elif data == 'Get current charge!\n':
#             power_metric = get_power_data()
#             charge_level = power_metric[4]
#             msg = str(charge_level)
             client_sock.send('100')
        elif data == 'Get current bat_volt!\n':
#             power_metric = get_power_data()
#             print(power_metric)
#             bat_volt = power_metric[0]
#             print(bat_volt)
#             msg = str(bat_volt)
#             print(msg)
#             client_sock.send(msg)
            client_sock.send('100')
        elif data == 'Get current charge_amps!\n':
            client_sock.send('100')
#             power_metric = get_power_data()
#             charge_amps = str(power_metric[1])
#             client_sock.send(charge_amps)
        elif data == 'Get current pan_watts!\n':
            client_sock.send('100')
#             power_metric = get_power_data()
#             pan_watts = str(power_metric[2])
#             client_sock.send(pan_watts)
        elif data == 'Get current pan_amps!\n':
            client_sock.send('100')
#             power_metric = get_power_data()
#             pan_amps = str(power_metric[3])
#             client_sock.send(pan_amps)
            


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