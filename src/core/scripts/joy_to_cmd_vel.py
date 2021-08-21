#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

max_vel_fwd = 1

def callback(msg):
    move = Twist()
    if msg.axes[1] > 0.2:
        print ("forward")
        move.linear.x = msg.axes[1] * max_vel_fwd 
    elif msg.axes[1] < -0.2:
        print ("backward")
        move.linear.x = -0.5
    elif msg.axes[3] > 0.2:
        print ("left")
        move.angular.z = 1.5
    elif msg.axes[3] < -0.2:
        move.angular.z = -1.5
        print ("right")

    cmd_vel_pub.publish(move)

rospy.init_node('run_from_joystick')

sub = rospy.Subscriber('joy', Joy, callback)

rospy.spin()
'''
red_light_twist = Twist()
red_light_twist.angular.z = 0.5
green_light_twist = Twist()
green_light_twist.linear.x = 0.5
driving_forward = False
light_change_time = rospy.Time.now()
rate = rospy.Rate(10)
print("m16a start")

while not rospy.is_shutdown():
    if driving_forward:
        rospy.logdebug("forward")
        print("m16a 1")
        cmd_vel_pub.publish(green_light_twist)
    else:
        print("m16a 2")
        rospy.logdebug("else")
        cmd_vel_pub.publish(red_light_twist)
    if light_change_time < rospy.Time.now():
        print("m16a 3")
        rospy.logdebug("switch")
        driving_forward = not driving_forward
        light_change_time = rospy.Time.now() + rospy.Duration(3)
    rate.sleep()

'''