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
    global angle_avg, distance, validUpdate
    angle_avg = 100
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
    # Find BFR
        hull, corners, BFR_img = MI.bestFitRect(img_orig, cnt) # when working take out drawing part of fn
        Contour_img = np.copy(BFR_img)
		
        # Check if Valid
        if MI.isValid(hull, corners):

            # Find and draw center
            cx, cy = MI.findCenter(hull, BFR_img)   # maybe use contour center instead of hull center...
            BFR_img = MI.drawCenterLine(BFR_img, cx,cy)
            
            # Find and display angle, distance, etc
            calculations = IC.imageMeasurements(BFR_img, cx, cy, corners)
            Rect_coor = calculations.organizeCorners()

            if MI.isValidAR(Rect_coor):
                angle = calculations.findAngle()
                distance = calculations.findDistance(Rect_coor)
                validUpdate = True
            else:
                validUpdate = False
                BFR_img = Contour_img
                print 'No Valid Update: AR wrong'
                
        else: # not valid
            validUpdate = False
            BFR_img = Contour_img
            print 'No Valid Update: Not enough corners or match_quality bad'
    else:
        validUpdate = False
        BFR_img = img_orig
        print 'No Valid Update: Contours not valid'
    
    
    return angle, distance, validUpdate, BFR_img, mask
