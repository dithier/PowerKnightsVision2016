# -*- coding: utf-8 -*-
"""
Created on Sat May 14 11:39:21 2016

@author: Ithier
"""

import HSVTrackbarModule as Trackbar
import cv2

# Directory of file containing initial threshold values
directory = 'C:/Users/Ithier/Documents/!!OpenCV/StrongHold Code/' # folder npz file is in
filename = directory + 'imageValues.npz'

img = cv2.imread('1.jpg', 1)

# Calibrate
Trackbar.calibrateCamera(img, filename)