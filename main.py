import ardrone
import sys
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
drone.setup()
drone.flat_trims()
time.sleep(1)

while True:

	
	
	cmd = getch()

	if ord(cmd) == 3:# looking for ctrl + c
		drone.disconect()
		sys.exit(0)

	
	if cmd == 'g':
		drone.land()
	elif cmd == 't':
		drone.take_off()
	elif cmd == 'a':
		drone.left()
	elif cmd == 'd':
		drone.right()
	elif cmd =='w'
		drone.foward()
	elif cmd == 's'
		drone.backward()
	elif cmd == 'i':
		drone.up()
	elif cmd == 'k'
		drone.down()
	elif cmd == 'j'
		drone.rotate_left()
	elif cmd == 'l'
		drone.rotate_right()
	elif cmd == 'e':
		drone.emergency_stop()
	else:
		pass


	#drone.emergency_stop()
	#time.sleep(.03) # dont overflow the queue
