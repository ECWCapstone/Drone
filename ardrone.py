import struct
import socket

import multiprocessing as mp
import time

# 5556 send
# 5554 receive navdata
CTRL_PORT = 5556
STATUS_PORT = 5554

class ARDrone:
	def __init__(self,IP_ADDRESS="192.168.1.1"):

		self.cmd_queue = mp.Queue()
		self.processes = []

		self.ip_address = IP_ADDRESS;
		self.ctrl_socket = socket.socket()
		self.status_socket = socket.socket()
		self.is_flying = mp.Value('b', False);
		self.is_emergency_mode = mp.Value('b', False);


	def connect(self):
		self.ctrl_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.status_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.status_socket.bind(('', STATUS_PORT))
		self.status_socket.sendto("\x01\x00\x00\x00", (self.ip_address, STATUS_PORT))

	def run(self):
		p = mp.Process(target=self.send_from_queue, args=(self.cmd_queue,))  # Queue dispatch thread 
		p2 = mp.Process(target=self.update_navdata, args=(self.is_flying,self.is_emergency_mode))  # Nav data listener thread

		self.processes.append(p)
		self.processes.append(p2)
		p.start()
		p2.start()

	def __set_navdata(self,flying,emergency_mode):
		drone_info = dict()
 		data = self.status_socket.recv(65535)
		navdata = struct.unpack_from("IIII", data, 0)

		flying = navdata[1] & 1 == 1
		emergency_mode = navdata[1] & 0x80000000 == 1

	def flat_trims(self):    # Levels the trim for flight !!! Must be on the ground, level!!!
		cmd_tup = ("FTRIM", "")
		self.cmd_queue.put(cmd_tup)

	def take_off(self):
		take_off_int = 0b10001010101000000001000000000
		cmd_tup = ("REF", (",%d" % take_off_int))
		self.cmd_queue.put(cmd_tup)

	def land(self):
		land_int = 0b10001010101000000000000000000
		cmd_tup = ("REF", (",%d" % land_int))
		self.cmd_queue.put(cmd_tup)

	def emergency_stop(self):
		stop_int = 0b10001010101000000000100000000
		cmd_tup = ("REF", (",%d" % stop_int))
		self.cmd_queue.put(cmd_tup)

	def hover(self):
		cmd_tup = ("PCMD", ",0,0,0,0,0")
		self.cmd_queue.put(cmd_tup)

	def send_ctrl_cmd(self,msg):
		self.ctrl_socket.sendto(msg, (self.ip_address,CTRL_PORT))

	def send_from_queue(self,queue):
		sequence_nbr = 1
		no_op_cmd = ("PCMD", ",0,0,0,0,0")
		while True:
			if queue.empty():
				msg = "AT*%s=%i%s\r" % (no_op_cmd[0],sequence_nbr,no_op_cmd[1])
				sequence_nbr += 1
				self.send_ctrl_cmd(msg)
				time.sleep(.5)

			else:
				cmd_tup = queue.get()
				msg = "AT*%s=%i%s\r" % (cmd_tup[0],sequence_nbr,cmd_tup[1])
				sequence_nbr += 1
				self.send_ctrl_cmd(msg)

			

	def update_navdata(self,flying,emergency_mode):
		while True:
			self.__set_navdata(flying,emergency_mode)
			time.sleep(.25)

	def __exit__(self,type,value,traceback):

		(thrd.cancel for thrd in self.threads)
		

		self.ctrl_socket.close()
		self.status_socket.close()
		