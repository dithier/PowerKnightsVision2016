# -*- coding: utf-8 -*-
"""
Created on Sat May 14 11:32:40 2016

@author: Ithier
"""

import HSVTrackbarModuleVideo as Trackbar
import cv2
import numpy as np

# Directory of file containing initial threshold values
directory = 'C:/Users/Ithier/Documents/!!OpenCV/StrongHold Code/' # folder npz file is in
filename = directory + 'imageValues.npz'
url = 'http://10.5.1.11/axis-cgi/mjpg/video.cgi?resolution=640x480'

Trackbar.initializeTrackbar(filename)

cap = cv2.VideoCapture(url) # capture laptop camera, 0 is laptop cam, numbers after that are cameras attached

 # Check to make sure cap was initialized in capture
if cap.isOpened():
    print 'Cap succesfully opened'
    print cap.grab()
else:
    print 'Cap initialization failed'

    
while(cap.isOpened()):
    ret, frame = cap.read()
    
    if frame is None:
        print 'Frame is None'
        Cam_frame = cv2.imread('1.png', 1)
        mask = Cam_frame
        lower_green, upper_green, scale = Trackbar.readImageValues(filename)
    else:
        Cam_frame = frame        
        mask, lower_green, upper_green, scale  = Trackbar.processImage(frame)
    
    cv2.imshow('image', mask)
    cv2.imshow('Camera', Cam_frame)
    k = cv2.waitKey(10) & 0xFF
    if k == ord('q'):
        break
    
 # Save values and exit program
np.savez(filename, brightness = scale, lower = lower_green, upper = upper_green) 
cap.release()      
cv2.destroyAllWindows()

