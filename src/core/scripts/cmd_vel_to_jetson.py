#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def callback(msg):
    if msg.linear.x > 0.2:
        print ("forward")
	cycle = translate(msg.linear.x, 0.2, 1, 80, 100)
        motor_left.ChangeDutyCycle(cycle)
        motor_right.ChangeDutyCycle(cycle)
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
