#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO

def callback(msg):
    if msg.linear.x > 0.2:
        print ("forward")
        motor_left.ChangeDutyCycle(70)
        motor_right.ChangeDutyCycle(70)
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

motor_left.steart(0)
motor_right.steart(0)

rospy.spin()