
import ardrone
import time

drone = ardrone.ARDrone()
time.sleep(.5)

drone.flat_trims()

while True:
	drone.set_navdata

	if not drone.is_flying:
		print "Not flying"
		drone.take_off()
	time.sleep(.03)
