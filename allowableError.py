# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 17:33:34 2016

@author: Ithier
"""

import math
towerHeight = 85 # inches
goalWidth = 16 # inches
ballRadius = 5 # inches
ball = ballRadius + 0.5 # put in factor of safety

def findError(distance):
    distD = math.sqrt((distance*12)**2 + towerHeight**2) # diagonal distance from camera to center of target
    angleError = math.atan(((goalWidth - 2*ball)/2)/distD)
    return angleError*(180.0/math.pi)
    

#Function documentation

#Triangle to goal
#		  *		<-Robot
#		 /|\    
#		/ | \
#	   /  |  \  <-longLeg (side)
#	  /___|___\ <-shortLeg(bottom)
#longLeg = distD / math.cos(angleError)
#shortLeg = 2 * math.sin(angleError) * distD

#distX = distance along the ground to the goal
#correction = buffer on either ends of the goal to get the correct allowed width of the target for aiming