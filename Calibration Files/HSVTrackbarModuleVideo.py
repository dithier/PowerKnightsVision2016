# -*- coding: utf-8 -*-
"""
Created on Wed May 11 11:15:30 2016

@author: Ithier
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 11:11:40 2016

@author: Ithier
"""
import cv2
import numpy as np

def initializeTrackbar(filename):
    def nothing(x):
        pass
    
    # Create window 
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    
    values = np.load(filename)
    brightness = float(values['brightness'])
    lower_bound = values['lower']
    upper_bound = values['upper']
    
    cv2.createTrackbar('Brightness', 'image', int(brightness*100), 100, nothing)
    cv2.createTrackbar('H_low', 'image', lower_bound[0], 255, nothing)
    cv2.createTrackbar('H_high', 'image', upper_bound[0], 255, nothing)
    cv2.createTrackbar('S_low', 'image', lower_bound[1], 255, nothing)
    cv2.createTrackbar('S_high', 'image', upper_bound[1], 255, nothing)
    cv2.createTrackbar('V_low', 'image', lower_bound[2], 255, nothing)
    cv2.createTrackbar('V_high', 'image', upper_bound[2], 255, nothing)
    
def readImageValues(filename):
    values = np.load(filename)
    brightness = float(values['brightness'])
    lower_bound = values['lower']
    upper_bound = values['upper']
    return lower_bound, upper_bound, brightness
 
# Darken image
def darken(scale, image):
    scale2 = scale/100.0
    darker = (image * scale2).astype(np.uint8)
    return darker, scale2
    
# Find HSV boundary values for mask
def findBounds():
    lower_green = np.array([cv2.getTrackbarPos('H_low', 'image'),cv2.getTrackbarPos('S_low', 'image'), cv2.getTrackbarPos('V_low', 'image')])
    upper_green = np.array([cv2.getTrackbarPos('H_high', 'image'),cv2.getTrackbarPos('S_high', 'image'), cv2.getTrackbarPos('V_high', 'image')])
    return lower_green, upper_green
    
def processImage(img):
    # Darken Image
    img, scale = darken(cv2.getTrackbarPos('Brightness', 'image'), img)
    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Define and apply threshold
    lower_green, upper_green= findBounds()
    mask = cv2.inRange(hsv,lower_green,upper_green)
    
    return mask, lower_green, upper_green, scale
    