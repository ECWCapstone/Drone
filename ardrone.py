import struct

class ARDrone:
	def __init__(self):
		self.is_flying = False;

	def set_navdata(self, data):
		drone_info = dict()

		navdata = struct.unpack_from("IIII", data, 0)

		self.is_flying = navdata[1] & 1 == 1