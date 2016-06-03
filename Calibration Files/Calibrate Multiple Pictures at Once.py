# -*- coding: utf-8 -*-
"""
Created on Wed May 11 13:46:31 2016

@author: Ithier
"""

import HSVTrackbarModuleMultiple as Trackbar

# DON'T FORGET TO ENTER: %matplotlib in consol before running

# Determine number of pictures you want to calibrate
imstart = 1

# Directory of file containing initial threshold values
directory = 'C:/Users/Driver/Desktop/OpenCV/StrongHold Code_Driver Station Version v2/' # folder npz file is in
filename = directory + 'imageValues.npz'

# Calibrate
Trackbar.calibrateCamera(imstart, filename)

