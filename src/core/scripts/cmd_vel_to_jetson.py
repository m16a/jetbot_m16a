#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO

def callback(msg):
    if msg.linear.x > 0.2:
        print ("forward")
        motor_left.ChangeDutyCycle(100 * msg.linear.x)
        motor_right.ChangeDutyCycle(100 * msg.linear.x)
        GPIO.output(12, GPIO.HIGH)
    else:
        motor_left.ChangeDutyCycle(0)
        motor_right.ChangeDutyCycle(0)
        GPIO.output(12, GPIO.LOW)

rospy.init_node('cmd_vel_to_jetson')
sub = rospy.Subscriber('cmd_vel', Twist, callback)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

motor_left = GPIO.PWM(32, 50000)
motor_right = GPIO.PWM(33, 50000)

motor_left.start(0)
motor_right.start(0)

rospy.spin()