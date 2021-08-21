#!/usr/bin/env python
from home.m16a.Desktop.ros.jetbot_m16a.src.core.scripts.joy_to_cmd_vel import MAX_VEL_FWD
import rospy
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO

MAX_VEL_FWD = 1

def callback(msg):
    if msg.linear.x > 0.2:
        print ("forward")
        motor_left.ChangeDutyCycle(100 * msg.linear.x)
        motor_right.ChangeDutyCycle(100 * msg.linear.x)
    else:
        motor_left.ChangeDutyCycle(0)
        motor_right.ChangeDutyCycle(0)

rospy.init_node('cmd_vel_to_jetson')
sub = rospy.Subscriber('cmd_vel', Twist, callback)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

motor_left = GPIO.PWM(32, 50000)
motor_right = GPIO.PWM(33, 50000)

motor_left.start(0)
motor_right.start(0)

rospy.spin()