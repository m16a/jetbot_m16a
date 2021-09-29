#!/usr/bin/env python
import rospy

#import time

import pygame
from pygame.locals import *

from geometry_msgs.msg import Twist

cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

max_lin_vel = 1
lin_acc = 0.05
lin_decay = 0.05

max_ang_vel = 1
ang_acc = 0.05
ang_decay = 0.05


pressedKeyEmpty = [0,0,0,0] # "wsad"
pressedKey = pressedKeyEmpty
current_move = Twist()

def handle_key(keys):
	global pressedKey
	if keys[K_w]:
		pressedKey[0] = 1
	if keys[K_s]:
		pressedKey[1] = 1
	if keys[K_a]:
		pressedKey[2] = 1
	if keys[K_d]:
		pressedKey[3] = 1
	
	#if (sum(pressedKey) != 0):
	#	print("handle key ")


def updateCurrentMove():
	global pressedKey
	global current_move
	#print("u")
	if pressedKey[0] == 0 and pressedKey[1] == 0:
		dirr = 1.0 if current_move.linear.x > 0 else -1.0
		prev = current_move.linear.x
		current_move.linear.x = current_move.linear.x - dirr * lin_decay
		#print(prev, ' ', current_move.linear.x)
		if prev * current_move.linear.x < 0.0:
			current_move.linear.x = 0.0
		#rospy.loginfo("stopping")
	else:
		if pressedKey[0] == 1:
			current_move.linear.x = min(current_move.linear.x + lin_acc, max_lin_vel)
		elif pressedKey[1] == 1:
			current_move.linear.x = max(current_move.linear.x - lin_acc, -max_lin_vel)
	
	if pressedKey[2] == 0 and pressedKey[3] == 0:
		dirr = 1.0 if current_move.angular.z > 0 else -1.0
		prev = current_move.angular.z
		current_move.angular.z = current_move.angular.z - dirr * ang_decay
		#print(prev, ' ', current_move.linear.x)
		if prev * current_move.angular.z < 0.0:
			current_move.angular.z = 0.0
		#rospy.loginfo("stopping")
	else:
		if pressedKey[2] == 1:
			current_move.angular.z = min(current_move.angular.z + ang_acc, max_ang_vel)
		elif pressedKey[3] == 1:
			current_move.angular.z = max(current_move.angular.z - ang_acc, -max_ang_vel)


	
	#rospy.loginfo(pressedKey)
	pressedKey = [0,0,0,0]

rospy.init_node('keyboard_to_cmd_vel')


def display(str):
    text = font.render(str, True, (255, 255, 255), (159, 182, 205))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery

    screen.blit(text, textRect)
    pygame.display.update()

pygame.init()
screen = pygame.display.set_mode( (640,480) )
pygame.display.set_caption('Python numbers')
screen.fill((159, 182, 205))
rate = rospy.Rate(30)

font = pygame.font.Font(None, 17)

num = 0
done = False
while not rospy.is_shutdown():
	pygame.event.pump()
	keys = pygame.key.get_pressed()
	if keys[K_ESCAPE]:
		handle_key(keys)
		break

	handle_key(keys)
	updateCurrentMove()
	cmd_vel_pub.publish(current_move)
	display( str(num) )
	num += 1
	rate.sleep()
	#print(num)



'''
if left pure
	left forward/right backward
'''