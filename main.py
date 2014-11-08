import ardrone
import sys
import signal
import time

import sys, tty, termios



##############################################################################################################
### WTF python, Really?
##############################################################################################################
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


drone = ardrone.ARDrone()
drone.connect()
drone.run()
drone.flat_trims()

while True:

	
	
	cmd = getch()

	if ord(cmd) == 3:     # looking for ctrl + c
		sys.exit(0)

	
	if cmd == 'l' or cmd == 'L':
		drone.land()
	elif cmd == 't':
		drone.take_off()
	else:
		pass


	#drone.emergency_stop()
	#time.sleep(.03) # dont overflow the queue
