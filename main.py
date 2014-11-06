import socket
import signal
import sys

import struct
import ardrone
import time

# 5556 send
# 5554 receive navdata

DRONE_IP = "192.168.1.1"
DRONE_PORT = 5556
DRONE_NAV_PORT = 5554


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print 'Connected to drone'

nav_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#nav_sock.setblocking(0)
nav_sock.bind(('', DRONE_NAV_PORT))
print 'Server socket set up'


def exit(signal, frame):
	#sock.shutdown()
	sock.sendto(drone.emergency_stop(),(DRONE_IP, DRONE_PORT))
	sock.close()

	#serversocket.shutdown()
	nav_sock.close()
	print "Cleaned up"
	sys.exit(0)

signal.signal(signal.SIGINT, exit)

drone = ardrone.ARDrone()
	

nav_sock.sendto("\x01\x00\x00\x00", (DRONE_IP, DRONE_NAV_PORT))

sock.sendto(drone.flat_trims_command(),(DRONE_IP,DRONE_PORT)) # Levels the trim for flight
time.sleep(.5)


while True:
	data = nav_sock.recv(65535)

	drone.set_navdata(data)

	if not drone.is_flying:
		print "Not flying"
		#print drone.take_off_command()
		sock.sendto(drone.take_off_command(),(DRONE_IP, DRONE_PORT))
	else:
		print "Flying"
		sock.sendto(drone.take_off_command(),(DRONE_IP, DRONE_PORT))
	time.sleep(.03)
