#!/usr/bin/env python
import rospy
import time
from PCA9685 import PCA9685

from geometry_msgs.msg import Twist

Dir = [
    'forward',
    'backward',
]

start_pwm = 0.5
pwn_len = 0

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

class MotorDriver():
    def __init__(self):
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4

    def MotorRun(self, motor, index, speed):
        if speed > 100:
            return
        if(motor == 0):
            pwm.setDutycycle(self.PWMA, speed)
            if(index == Dir[0]):
                pwm.setLevel(self.AIN1, 0)
                pwm.setLevel(self.AIN2, 1)
            else:
                pwm.setLevel(self.AIN1, 1)
                pwm.setLevel(self.AIN2, 0)
        else:
            pwm.setDutycycle(self.PWMB, speed)
            if(index == Dir[0]):
                pwm.setLevel(self.BIN1, 0)
                pwm.setLevel(self.BIN2, 1)
            else:
                pwm.setLevel(self.BIN1, 1)
                pwm.setLevel(self.BIN2, 0)

    def MotorStop(self, motor):
        if (motor == 0):
            pwm.setDutycycle(self.PWMA, 0)
        else:
            pwm.setDutycycle(self.PWMB, 0)

def on_cmd_vel(msg):
    vel_left = msg.linear.x + msg.angular.z
    vel_left = clamp(vel_left, -1.0, 1.0)
    vel_right = msg.linear.x - msg.angular.z
    vel_right = clamp(vel_right, -1.0, 1.0)

    if abs(vel_left) < 0.1:
        rospy.loginfo("m16a left stop")
        Motor.MotorStop(0)
    else:
	value = 100 * min(1, translate(abs(vel_left), 0, 1, 0, 0.5) + start_pwm)
        rospy.loginfo("left {} {}".format('f' if vel_left > 0 else 'b', value))
        Motor.MotorRun(0, 'forward' if vel_left  > 0.0 else 'backward', value)

    if abs(vel_right) < 0.1:
        rospy.loginfo("m16a right stop")
        Motor.MotorStop(1)
    else:
	value = 100 * min(1, translate(abs(vel_right), 0, 1, 0, 0.5) + start_pwm)
        rospy.loginfo("right {} {}".format('f' if vel_right > 0 else 'b', value))
        Motor.MotorRun(1, 'forward' if vel_right > 0.0 else 'backward', value)
	

    

try:
    pwm = PCA9685(0x40, debug=False)
    pwm.setPWMFreq(50)

    Motor = MotorDriver()

    # setup ros node
    rospy.init_node('jetbot_motors')
    sub = rospy.Subscriber('cmd_vel', Twist, on_cmd_vel)

    # start running
    rospy.spin()

    Motor.MotorStop(0)
    Motor.MotorStop(1)

except IOError as e:
    print(e)

except KeyboardInterrupt:    
    print("\r\nctrl + c:")
    Motor.MotorStop(0)
    Motor.MotorStop(1)
    exit()


