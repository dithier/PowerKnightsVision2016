# -*- coding: utf-8 -*-
"""
Created on Tue May 17 23:10:52 2016

@author: Ithier
"""

import FindTargetModule as FTM
import cv2

directory = 'C:/Users/Ithier/Documents/OpenCV/FIRST 2016/PowerKnightsVision2016/'
#directory = 'C:/Users/Ithier/Documents/!!OpenCV/Mayhem/' # folder npz file is in
filename = directory + 'imageValues.npz'

frame = cv2.imread('1.jpg', 1)

# Create resizable window for camera 
cv2.namedWindow('Camera Frame', cv2.WINDOW_NORMAL)

# Rotate image
rows, cols, dim = frame.shape
M = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1) # image center, angle, scaling  factor 
frame = cv2.warpAffine(frame,M,(cols,rows))
  
# Process image
Angle, Distance, validUpdate, Processed_frame, mask = FTM.findTarget(frame,filename)

if -1 <= Angle <= 1:
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(Processed_frame,'LOCKED',(90,400), font, 3.8,(0,255,0),6,cv2.LINE_AA)
        
    



# Display the resulting frame
cv2.imshow('Camera Frame', Processed_frame)
cv2.imshow('Mask', mask)
   
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()