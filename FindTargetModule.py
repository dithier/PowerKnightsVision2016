# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:59:58 2016

@author: Ithier
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 11 11:09:44 2016

@author: Ithier
"""


import cv2
import numpy as np
import manipulateImageModule as MI 
import imageCalculationsClass as IC


def findTarget(img_orig, filename):
    global angle, distance, validUpdate
    angle = 1000
    distance = 0
    validUpdate = False
    
    # Make copy of frame/image to work with
    img = np.copy(img_orig)
    
    # Load calibration parameters
    values = np.load(filename)
    brightness = float(values['brightness'])
    lower_bound = values['lower']
    upper_bound = values['upper']
    
    # Create img with parameters
    img_darker = MI.darkenImage(img, brightness)
    hsv = cv2.cvtColor(img_darker, cv2.COLOR_BGR2HSV)
    mask_orig = cv2.inRange(hsv,lower_bound,upper_bound)
    
    mask= mask_orig[:]
    
    # Clean up mask with dilate and erode and threshold
    mask = MI.dilateAndErode(mask, 5)
    maskc = np.copy(mask)
    ret,maskc = cv2.threshold(maskc,127,255,0)
    
    # Find contours
    cnt, contours, valid = MI.contours(img_orig, maskc)

    if valid: 
        validUpdate = True
        
        # Find BFR
        hull, corners, BFR_img = MI.bestFitRect(img_orig, cnt) 
      
        # Find and draw center
        cx, cy = MI.findCenter(hull, BFR_img)  
        BFR_img = MI.drawCenterLine(BFR_img, cx,cy)
                
        # Find and display angle, distance, etc
        calculations = IC.imageMeasurements(BFR_img, cx, cy, corners)
        Rect_coor = calculations.organizeCorners()
        angle = calculations.findAngle()
        distance = calculations.findDistance(Rect_coor)
               
    else:
        validUpdate = False
        BFR_img = img_orig
        print 'No Valid Update'
    
    
    return angle, distance, validUpdate, BFR_img, mask
