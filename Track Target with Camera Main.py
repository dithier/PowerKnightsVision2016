# -*- coding: utf-8 -*-
"""
Created on Fri May 13 18:10:44 2016

@author: Ithier
"""

import FindTargetModule as FTM
import NetworkTableModule as NT
import time
import cv2

directory = 'C:/Users/Driver/Desktop/OpenCV/StrongHold Code_Driver Station Version v2/' # folder npz file is in
frame_0 = directory + 'Raw/'
frame_p = directory + 'Processed/'
filename = directory + 'imageValues.npz'
url = 'http://10.5.1.11/axis-cgi/mjpg/video.cgi?resolution=640x480'
#############################################################################
from networktables import NetworkTable
import logging

if NetworkTable._staticProvider is None:
    logging.basicConfig(level=logging.DEBUG)
    NetworkTable.setIPAddress('10.5.1.2')
    NetworkTable.setClientMode()
    NetworkTable.initialize()

sd = NetworkTable.getTable("Camera")
##############################################################################

cap = cv2.VideoCapture(url) # capture laptop camera, 0 is laptop cam, numbers after that are cameras attached

 # Check to make sure cap was initialized in capture
if cap.isOpened():
    print 'Cap succesfully opened'
    print cap.grab()
else:
    print 'Cap initialization failed'

    
# Create resizable window for camera 
cv2.namedWindow('Camera Frame', cv2.WINDOW_NORMAL)

while(cap.isOpened()):
    # Determine time stamp
    t = time.localtime()
    stamp = str(t[1]) + "_" + str(t[2]) + "_" + str(t[0]) + "time_" + str(t[3]) + "_" + str(t[4]) + "_" + str(t[5])
    # save only every 15 images?
   
    # Capture frame-by-frame
    #    ret returns true or false (T if img read correctly); frame is array of img    
    ret, frame = cap.read()
    
    if frame is None:
        print 'Frame is None'
        Processed_frame = cv2.imread('1.png', 1)
        mask = Processed_frame
    else:
        try:
            # Save orignal frame
            cv2.imwrite(frame_0 + stamp + '.jpg', frame)
        
            # Rotate image
            rows, cols, dim = frame.shape
            M = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1) # image center, angle, scaling  factor 
            Rotated_frame = cv2.warpAffine(frame,M,(cols,rows))
        
            # Process image
            Angle, Distance, validUpdate, Processed_frame, mask = FTM.findTarget(Rotated_frame,filename)
            
            if -0.3 <= Angle <= 0.3:
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(Processed_frame,'LOCKED',(180,400), font, 3.5,(0,0,255),4,cv2.LINE_AA)
            
            # Send to NetworkTable
            NT.sendValues(sd, Angle, Distance, validUpdate)
            
            # Put crosshairs on image
            rows, cols, dim = Processed_frame.shape
            cv2.line(Processed_frame, (cols/2,0), (cols/2,rows), (255,0,0), 2)
            cv2.line(Processed_frame, (0,rows/2), (cols,rows/2), (255,0,0), 2)
            
            # Save processed frame
            cv2.imwrite(frame_p + stamp + '.jpg', Processed_frame)
            
        except:
            print 'There was an error'
    
    # Display the resulting frame
    cv2.imshow('Camera Frame', Processed_frame)
    cv2.imshow('Mask', mask)
   
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
     
    
# When capture done, release it
cap.release() # !! important to do
cv2.destroyAllWindows()


