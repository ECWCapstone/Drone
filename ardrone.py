import struct

class ARDrone:
	def __init__(self):
		self.sequence_nbr = 1;
		self.is_flying = False;
		self.is_emergency_mode = False;

	def set_navdata(self, data):
		drone_info = dict()
 
		navdata = struct.unpack_from("IIII", data, 0)

		self.is_flying = navdata[1] & 1 == 1
		self.is_emergency_mode = navdata[1] & 0x80000000 == 1

	def flat_trims_command(self):
		msg = "AT*FTRIM=%d\r" % self.sequence_nbr
		self.sequence_nbr += 1
		return msg

	def take_off_command(self):
		take_off_int = 0b10001010101000000001000000000
		msg = "AT*REF=%i,%d\r" % (self.sequence_nbr, take_off_int)
		self.sequence_nbr += 1
		return msg

	def land_command(self):
		land_int = 0b10001010101000000000000000000
		msg = "AT*REF=%i,%d\r" % (self.sequence_nbr, land_int)
		self.sequence_nbr += 1
		return msg

	def emergency_stop (self):
		stop_int = 0b10001010101000000000100000000
		msg =  "AT*REF=%i,%d\r" % (self.sequence_nbr, stop_int)
		self.sequence_nbr += 1
		return msg
