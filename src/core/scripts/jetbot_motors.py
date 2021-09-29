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
    vel_right = msg.linear.x - msg.angular.z

    if abs(vel_left) < 0.1:
        rospy.loginfo("m16a left stop")
        Motor.MotorStop(0)

    if abs(vel_right) < 0.1:
        rospy.loginfo("m16a right stop")
        Motor.MotorStop(1)

    Motor.MotorRun(0, 'forward' if vel_left  > 0.0 else 'backward', 100 * min(1, abs(vel_left) + start_pwm))
    Motor.MotorRun(1, 'forward' if vel_right > 0.0 else 'backward', 100 * min(1, abs(vel_right) + start_pwm))

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


