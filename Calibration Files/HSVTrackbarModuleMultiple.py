# -*- coding: utf-8 -*-
"""
Created on Wed May 11 13:50:42 2016

@author: Ithier
"""

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
import matplotlib.pyplot as plt
import matplotlib.animation as animation

 
def calibrateCamera(imstart, filename):
    # Set up images you want to analyze
    images= []
    for i in range(imstart, imstart + 9):
        name = str(i) + '.jpg'
        images.append(cv2.imread(name, 1))
    
    # Create windows
    cv2.namedWindow('Trackbar', cv2.WINDOW_NORMAL)
    fig = plt.figure()
    
    def nothing(x):
        pass
    
    # Darken image
    def darken(scale, image):
        scale2 = scale/100.0
        darker = (image * scale2).astype(np.uint8)
        return darker, scale2
        
    # Find HSV boundary values for mask
    def findBounds():
        lower_green = np.array([cv2.getTrackbarPos('H_low', 'Trackbar'),cv2.getTrackbarPos('S_low', 'Trackbar'), cv2.getTrackbarPos('V_low', 'Trackbar')])
        upper_green = np.array([cv2.getTrackbarPos('H_high', 'Trackbar'),cv2.getTrackbarPos('S_high', 'Trackbar'), cv2.getTrackbarPos('V_high', 'Trackbar')])
        return lower_green, upper_green
    
    def processImage(IMG):
        global scale, lower_green, upper_green
        # Darken image
        img, scale = darken(cv2.getTrackbarPos('Brightness', 'Trackbar'), IMG)
        
        # Convert to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Define and apply threshold
        # green in hsv is [60 255 255]
        lower_green, upper_green= findBounds()
        mask = cv2.inRange(hsv,lower_green,upper_green) 
        return mask, lower_green, upper_green, scale 
        
    def readValues(filename):
        global scale, lower_green, upper_green
        values = np.load(filename)
        scale = float(values['brightness'])
        lower_green = values['lower']
        upper_green = values['upper']
        return lower_green, upper_green, scale
    
    # http://matplotlib.org/1.5.1/examples/animation/dynamic_image.html
    def updateDisplay(fig, mask, i):
        ax = fig.add_subplot(3,3,i+1)
        ax.set_xticks([])
        ax.set_yticks([])
        im = ax.imshow(mask[i], animated = True) 
        
        def updatefig(*args):
            im.set_array(mask[i])
            return im,
            
        animation.FuncAnimation(fig, updatefig, blit = True)
    
        # create trackbars for color change
    #   trackbar name, window name its attached to, default val,
    #       max value, callback fn which is executed each time trackbar val changes
    #         Load values from last use to start with
    values = np.load(filename)
    brightness = float(values['brightness'])
    lower_bound = values['lower']
    upper_bound = values['upper']
    
    cv2.createTrackbar('Brightness', 'Trackbar', int(brightness*100), 100, nothing)
    cv2.createTrackbar('H_low', 'Trackbar', lower_bound[0], 255, nothing)
    cv2.createTrackbar('H_high', 'Trackbar', upper_bound[0], 255, nothing)
    cv2.createTrackbar('S_low', 'Trackbar', lower_bound[1], 255, nothing)
    cv2.createTrackbar('S_high', 'Trackbar', upper_bound[1], 255, nothing)
    cv2.createTrackbar('V_low', 'Trackbar', lower_bound[2], 255, nothing)
    cv2.createTrackbar('V_high', 'Trackbar', upper_bound[2], 255, nothing)
    
    # creat switch for functionality
    switch = '0: OFF \n 1: ON'
    cv2.createTrackbar(switch, 'Trackbar', 0, 1, nothing)
    
    
    
    while(1):
        
        sw = cv2.getTrackbarPos(switch, 'Trackbar')
        mask = []
        if sw == 1:
            for i in range(0,len(images)):
                mask_i, lower_green, upper_green, scale  = processImage(images[i])
                mask.append(mask_i)
                
            test, lg, ug, s = processImage(cv2.imread('1.jpg')) 
            
        else:
            lower_green, upper_green, scale = readValues(filename)
            for i in range(0,len(images)):
                b,g,r = cv2.split(images[i])
                im = cv2.merge([r,g,b])
                mask.append(im)
                
            test = images[0]
            
        
        # Display masks
        for i in range(0, len(mask)):
            updateDisplay(fig, mask, i)
        
        plt.show()
        
        cv2.imshow('Trackbar', test)
        k = cv2.waitKey(10) & 0xFF
        if k == ord('q'):
            break 
        
        
     # Save values and exit program
    cv2.destroyAllWindows()
    plt.close()
    np.savez(filename, brightness = scale, lower = lower_green, upper = upper_green)       
    