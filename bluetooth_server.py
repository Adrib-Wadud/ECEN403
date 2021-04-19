from bluetooth import *

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

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
 
try:
    while True:
        data = client_sock.recv(1024)
	
        if len(data) == 0: break
        print(data)
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
	   if fan_speed < 100:
	   	fan_speed = fan_speed + 25
           	client_sock.send('Fan speed up command received')
	   elif fan_speed == 100:
                client_sock.send('Max Fan speed reached')
	elif data == 'Fan Speed Down!\n':
	   if fan_speed > 0 :
		fan_speed = fan_speed - 25
		client_sock.send('Fan speed down command received')
           elif fan_speed == 0:
                client_sock.send('Fan OFF')
	elif data == 'Humidifier Intensity Up!\n':
	   if humidity_intensity < 4:
	   	humidity_intensity = humidity_intensity + 1
           	client_sock.send('Humidifier intensity up command received')
	   elif humidity_intensity == 4:
		client_sock.send('Max humidifier intensity reached')
	elif data == 'Humidifier Intensity Down!\n':
	   if humidity_intensity > 0:
                humidity_intensity = humidity_intensity - 1
                client_sock.send('Humidifier intensity down command received')
           elif humidity_intensity == 0:
                client_sock.send('Humidifier OFF')
        elif data == 'Deactivate Manual Mode!\n':
           client_sock.send('Manual Mode deactivation command received')
        elif data == 'Deactivate Auto Mode!\n':
           client_sock.send('Auto mode deactivation command received')
	elif data == 'Get current temperature!\n':
	   msg = str(curr_temperature) + ' F'
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

except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
