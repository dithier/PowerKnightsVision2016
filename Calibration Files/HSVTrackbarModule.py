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

 
def calibrateCamera(image, filename):
    global scale, lower_green, upper_green 
    scale = 100
    lower_green = []
    upper_green = []
    
    # Create window 
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    
    def nothing(x):
        pass

    # Darken image
    def darken(scale):
        scale2 = scale/100.0
        darker = (image * scale2).astype(np.uint8)
        return darker, scale2
        
    # Find HSV boundary values for mask
    def findBounds():
        lower_green = np.array([cv2.getTrackbarPos('H_low', 'image'),cv2.getTrackbarPos('S_low', 'image'), cv2.getTrackbarPos('V_low', 'image')])
        upper_green = np.array([cv2.getTrackbarPos('H_high', 'image'),cv2.getTrackbarPos('S_high', 'image'), cv2.getTrackbarPos('V_high', 'image')])
        return lower_green, upper_green

        # create trackbars for color change
#   trackbar name, window name its attached to, default val,
#       max value, callback fn which is executed each time trackbar val changes
#         Load values from last use to start with
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
    
    # creat switch for functionality
    switch = '0: OFF \n 1: ON'
    cv2.createTrackbar(switch, 'image', 0, 1, nothing)
    
    while(1):
        
        sw = cv2.getTrackbarPos(switch, 'image')
        
        if sw == 1:
            # Darken Image
            img, scale = darken(cv2.getTrackbarPos('Brightness', 'image'))
        
            # Convert to HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Define and apply threshold
            # green in hsv is [60 255 255]
            global lower_green, upper_green
            lower_green, upper_green= findBounds()
            mask = cv2.inRange(hsv,lower_green,upper_green)
        else:
            mask = image
         
        cv2.imshow('image', mask)
        k = cv2.waitKey(10) & 0xFF
        if k == ord('q'):
            break
        
     # Save values and exit program
    np.savez(filename, brightness = scale, lower = lower_green, upper = upper_green)       
    cv2.destroyAllWindows()
