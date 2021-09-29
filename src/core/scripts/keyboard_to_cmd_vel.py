#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

import time
import sys
import select
import tty
import termios


cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

max_vel_fwd = 1
acc = 0.01;
decay = 0.1;
pressedKeyEmpty = [0,0,0,0] # "wsad"
pressedKey = pressedKeyEmpty
current_move = Twist()

def handle_key(key):
	global pressedKey
	if key == 'w': #W
		pressedKey[0] = 1;
	if key == 's': #S
		pressedKey[1] = 1;
	if key == 'a': #A
		pressedKey[2] = 1;
	if key == 'd': #D
		pressedKey[3] = 1;		
	
	#print("handle key ", key)


def updateCurrentMove():
	global pressedKey
	global current_move
	#print("u")
	if pressedKey[0] == 0 and pressedKey[1] == 0 and current_move.linear.x != 0.0:
		dirr = 1.0 if current_move.linear.x > 0 else -1.0
		prev = current_move.linear.x;
		current_move.linear.x = current_move.linear.x - dirr * decay
		#print(prev, ' ', current_move.linear.x)
		if prev * current_move.linear.x < 0.0:
			current_move.linear.x = 0.0
		#rospy.loginfo("stopping")

	else:

		if pressedKey[0] == 1:
			current_move.linear.x = min(current_move.linear.x + acc, max_vel_fwd);
		elif pressedKey[1] == 1:
			current_move.linear.x = max(current_move.linear.x - acc, -max_vel_fwd);
	#rospy.loginfo(pressedKey)
	pressedKey = [0,0,0,0]

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

old_settings = termios.tcgetattr(sys.stdin)


rospy.init_node('keyboard_to_cmd_vel')
#rate = rospy.Rate(10)#try removing this line ans see what happens

tty.setcbreak(sys.stdin.fileno())
try:
	while not rospy.is_shutdown():
		updateCurrentMove()
		cmd_vel_pub.publish(current_move)
		#print(current_move)		
		if isData():
			c = sys.stdin.read(1)
			#print(c)
			handle_key(c)
			if c == '\x1b':         # x1b is ESC
				break

#			time.sleep(0.01)
		
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)



