import struct
import socket

# 5556 send
# 5554 receive navdata
CTRL_PORT = 5556
STATUS_PORT = 5554

class ARDrone:
	def __init__(self,IP_ADDRESS="192.168.1.1"):
		self.sequence_nbr = 1;
		self.ip_address = IP_ADDRESS;
		self.ctrl_socket = socket.socket()
		self.status_socket = socket.socket()
		self.is_flying = False;
		self.is_emergency_mode = False;


	def connect(self):
		self.ctrl_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.status_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.status_socket.bind(('', STATUS_PORT))
		self.status_socket.sendto("\x01\x00\x00\x00", (self.ip_address, STATUS_PORT))

	def set_navdata(self):
		drone_info = dict()
 		data = self.status_socket.recv(65535)
		navdata = struct.unpack_from("IIII", data, 0)

		self.is_flying = navdata[1] & 1 == 1
		self.is_emergency_mode = navdata[1] & 0x80000000 == 1

	def flat_trims(self):    # Levels the trim for flight !!! Must be on the ground, level!!!
		msg = "AT*FTRIM=%d\r" % self.sequence_nbr
		self.sequence_nbr += 1
		self.send_ctrl_cmd(msg)

	def take_off(self):
		take_off_int = 0b10001010101000000001000000000
		msg = "AT*REF=%i,%d\r" % (self.sequence_nbr, take_off_int)
		self.sequence_nbr += 1
		self.send_ctrl_cmd(msg)

	def land(self):
		land_int = 0b10001010101000000000000000000
		msg = "AT*REF=%i,%d\r" % (self.sequence_nbr, land_int)
		self.sequence_nbr += 1
		self.send_ctrl_cmd(msg)

	def emergency_stop(self):
		stop_int = 0b10001010101000000000100000000
		msg =  "AT*REF=%i,%d\r" % (self.sequence_nbr, stop_int)
		self.sequence_nbr += 1
		self.send_ctrl_cmd(msg)

	def send_ctrl_cmd(self,msg):
		self.ctrl_socket.sendto(msg, (self.ip_address,CTRL_PORT))

	def __exit__(self,type,value,traceback):
		self.ctrl_socket.close()
		self.status_socket.close()
		