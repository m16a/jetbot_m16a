#!/usr/bin/env python
import rospy
from getch import getch
from geometry_msgs.msg import Twist

cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

max_vel_fwd = 1

def on_key(key):
	move = Twist()	
	if key == 119: #W
		print ("forward")
		move.linear.x = max_vel_fwd
	elif key == 97: #A
		print ("left")
		move.angular.z = 1.5
	elif key == 115: #S
		print ("backward")
		move.linear.x = -0.5
	elif key == 100: #D
		move.angular.z = -1.5
		print ("right")

	cmd_vel_pub.publish(move)


#pub = rospy.Publisher('key',Int8,queue_size=10) # "key" is the publisher name
rospy.init_node('keypress',anonymous=True)
rate = rospy.Rate(10)#try removing this line ans see what happens
while not rospy.is_shutdown():
	key = ord(getch())
	if key == 27: #ESC
		break
	on_key(key)

            #rospy.loginfo(str(k))# to print on  terminal 
            #pub.publish(k)#to publish
        #rospy.loginfo(str(k))

#rospy.spin()

