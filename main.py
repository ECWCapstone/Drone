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
time.sleep(3)

print "Drone ready"

while True:

	try: 
		cmd = getch()

		if ord(cmd) == 3:# looking for ctrl + c
			drone.disconect()
			sys.exit(0)

		
		if cmd == 'g':
			drone.land()
		elif cmd == 't':
			print "Taking off"
			drone.take_off()
		elif cmd == 'a':
			drone.left()
		elif cmd == 'd':
			drone.right()
		elif cmd =='w':
			drone.forward()
		elif cmd == 's':
			drone.backward()
		elif cmd == 'i':
			drone.up()
		elif cmd == 'k':
			drone.down()
		elif cmd == 'j':
			drone.rotate_left()
		elif cmd == 'l':
			drone.rotate_right()
		elif cmd == 'e':
			drone.emergency_stop()
		else:
			pass
	except Exception as e:
		print type(e)           
		print "It was Will's fault"
	#drone.emergency_stop()
	#time.sleep(.03) # dont overflow the queue
