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
	   client_sock.send('Temperature up command received')
        elif data == 'Temperature Down!\n':
           client_sock.send('Temperature down command received')
	elif data == 'Humidity Up!\n':
           client_sock.send('Humidity up command received')
	elif data == 'Humidity Down!\n':
           client_sock.send('Humidty down command received')
	elif data == 'Fan Speed Up!\n':
           client_sock.send('Fan speed up command received')
	elif data == 'Fan Speed Down!\n':
           client_sock.send('Fan speed down command received')
	elif data == 'Humidifier Intensity Up!\n':
           client_sock.send('Humidifier intensity up command received')
	elif data == 'Humidifier Intensity Down!\n':
           client_sock.send('Humidifier intensity down command received')
        elif data == 'Deactivate Manual Mode!\n':
           client_sock.send('Manual Mode deactivation command received')
        elif data == 'Deactivate Auto Mode!\n':
           client_sock.send('Auto mode deactivation command received')
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
