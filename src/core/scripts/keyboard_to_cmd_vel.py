#!/usr/bin/env python
import rospy
import threading
import time
from getch import getch
from geometry_msgs.msg import Twist

cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

max_vel_fwd = 1
acc = 0.01;
decay = 0.1;
pressedKeyEmpty = [0,0,0,0] # "wsad"
pressedKey = pressedKeyEmpty
current_move = Twist()

def handle_key():
	while True:
		key = ord(getch())
		if key == 27: #ESC
			exit(0)

		if key == 119: #W
			pressedKey[0] = 1;
		if key == 115: #S
			pressedKey[1] = 1;
		if key == 97: #A
			pressedKey[2] = 1;
		if key == 100: #D
			pressedKey[3] = 1;
		
		time.sleep(0.01)
		rospy.loginfo("key was handled")
		


def updateCurrentMove():
	global pressedKey
	global current_move
	if pressedKey[0] == 0 and pressedKey[1] == 0 and current_move.linear.x != 0.0:
		dirr = 1.0 if current_move.linear.x > 0 else -1.0
		prev = current_move.linear.x;
 		current_move.linear.x = current_move.linear.x - dirr * decay
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

rospy.init_node('keyboard_to_cmd_vel')
rate = rospy.Rate(10)#try removing this line ans see what happens
th = threading.Thread(target=handle_key)
th.start()

while not rospy.is_shutdown():
	updateCurrentMove()
	cmd_vel_pub.publish(current_move)		

	time.sleep(0.05)
	
th.join()
            #rospy.loginfo(str(k))# to print on  terminal 
            #pub.publish(k)#to publish
        #rospy.loginfo(str(k))

#rospy.spin()

