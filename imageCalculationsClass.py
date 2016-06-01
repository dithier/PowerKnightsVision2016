# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 17:03:57 2016

@author: Ithier
"""
import cv2 
import math 
from collections import Counter

class imageMeasurements:

    def __init__(self, image, cx, cy, corners):
        self.image = image
        self.cx = cx
        self.cy = cy
        self.corners = corners
        
    def organizeCorners(self):
        
        def saveCoordinates(topLeftX, topLeftY, topRightX, topRightY, bottomRightX, bottomRightY, bottomLeftX, bottomLeftY):
            Rect_coor = []
            for i in range(0,4):
                Rect_coor.append([])    
            Rect_coor[0].append(topLeftX)
            Rect_coor[0].append(topLeftY)
            Rect_coor[1].append(topRightX)
            Rect_coor[1].append(topRightY)
            Rect_coor[2].append(bottomRightX)
            Rect_coor[2].append(bottomRightY)
            Rect_coor[3].append(bottomLeftX)
            Rect_coor[3].append(bottomLeftY)
            return Rect_coor
            
        # Determine correct order of corner coordinates 
        #       Determine x coordinates
        corners2 = list(self.corners.ravel())
        x = []
                
        for i in xrange(0, len(corners2), 2):
            x.append(corners2[i])
        
        # Check for duplicate and find value
        duplicate = len(x) != len(set(x))
        c = Counter(x).items()
        doubleVal = []
        if len(c) == 2:
            doubleVal.append(c[0][0])
            doubleVal.append(c[1][0])
            doubleVal.sort()
        elif len(c) == 3:
            for i in range(0,len(c)):
                if c[i][1] == 2:
                    doubleVal.append(c[i][0])
                    break
        
        # Determine if repeat number is max or min in array
        if len(doubleVal) > 0:
            maximum = max(x) == doubleVal[0]
                
        # Find top right and bottom right coordinates
        #     find the indices for the two right corners
        if duplicate:
            if len(doubleVal) == 1:
                if maximum:
                    indices = [i for i, a in enumerate(x) if a == doubleVal[0]]
                    maxXind = indices[0]
                    secMaxXind = indices[1]
                else: 
                    maxXind = x.index(max(x))
                    copy = x[:]
                    copy.pop(maxXind)
                    secMaxVal = max(copy)
                    secMaxXind = x.index(secMaxVal)
            else:
                indices = [i for i, a in enumerate(x) if a == doubleVal[1]]
                maxXind = indices[0]
                secMaxXind = indices[1]
        else:
            maxXind = x.index(max(x))
            copy = x[:]
            copy.pop(maxXind)
            secMaxVal = max(copy)
            secMaxXind = x.index(secMaxVal)
            
        #     determine which index is top and by default is bottom
        if corners2[maxXind*2 + 1] > corners2[secMaxXind*2 + 1]:
            topRightX = x[secMaxXind]
            topRightY = corners2[secMaxXind*2 + 1]
            bottomRightX = x[maxXind]
            bottomRightY = corners2[maxXind*2 + 1]
        else: 
            bottomRightX = x[secMaxXind]
            bottomRightY = corners2[secMaxXind*2 + 1]
            topRightX = x[maxXind]
            topRightY = corners2[maxXind*2 + 1]
                    
        # Find top left and bottom left coordinates
        if duplicate:
            if len(doubleVal) == 1:
                if not maximum:
                    indices = [i for i, a in enumerate(x) if a == doubleVal[0]]
                    minXind = indices[0]
                    secMinXind = indices[1]
                else: 
                    minXind = x.index(min(x))
                    copy = x[:]
                    copy.pop(minXind)
                    secMinVal = min(copy)
                    secMinXind = x.index(secMinVal)
            else:
                indices = [i for i, a in enumerate(x) if a == doubleVal[0]]
                minXind = indices[0]
                secMinXind = indices[1]
        else:
            minXind = x.index(min(x))
            copy = x[:]
            copy.pop(minXind)
            secMinVal = min(copy)
            secMinXind = x.index(secMinVal)
        #     determine which index is top and by default is bottom
        if corners2[minXind*2 + 1] > corners2[secMinXind*2 + 1]:
            topLeftX = x[secMinXind]
            topLeftY = corners2[secMinXind*2 + 1]
            bottomLeftX = x[minXind]
            bottomLeftY = corners2[minXind*2 + 1]
        else: 
            bottomLeftX = x[secMinXind]
            bottomLeftY = corners2[secMinXind*2 + 1]
            topLeftX = x[minXind]
            topLeftY = corners2[minXind*2 + 1]
                
        # Save Coordinates in Proper Order  
        Rect_coor = saveCoordinates(topLeftX, topLeftY, topRightX, topRightY, bottomRightX, bottomRightY, bottomLeftX, bottomLeftY)
        return Rect_coor
            
        
    def findAngle(self):
        global horizontal_cameraFOV, vertical_cameraFOV 
        global h,w,c
        global font
        horizontal_cameraFOV = 47.0
        vertical_cameraFOV = 36.5
        
        h, w, c = self.image.shape # h = height, w = width, c = channel
        offsetpx = (w/2.0) - self.cx # offset from center of camera image to center of target (pixels)
        
        angle_w = horizontal_cameraFOV * (offsetpx / w)
        angle = angle_w*(180.0/47.0)
        
        font = cv2.FONT_HERSHEY_COMPLEX
        self.image = cv2.putText(self.image,'Angle_avg: ' + str(angle),(10,50), font, 0.5,(0,0,255),1,cv2.LINE_AA)

        return angle
    
    def changeCoor(self):
        centerX = w/2.0
        centerY = h/2.0
        
        X_LocationD = (self.cx - centerX) / centerX
        X_LocationD = int(X_LocationD*100.0)/100.0
        
        Y_LocationD = -(self.cy - centerY) / centerY
        Y_LocationD = int(Y_LocationD*100.0)/100.0
        
        self.image = cv2.putText(self.image,'Center Location: (' + str(X_LocationD) + ', ' + str(Y_LocationD) + ')',(10,300), font, 0.5,(0,0,255),1,cv2.LINE_AA)
        return X_LocationD, Y_LocationD     
        
        
    def findDistance(self, Rect_coor):
        towerH = (89/12) # height from ground to center of target (in real life) in ft
        
        # dimensions from target (from game manual)
        targetWidth = 20.0 # in
        
        def Distance(targetActual, imagePx, targetPx, cameraFOV):
            robot2camera = 1.5 # ft    distance from front of robot to camera (so that distance calculation is distance from tower to front of robot)
            totalDistance = (((targetActual*imagePx)/targetPx)/2.0) / \
        			math.tan(((cameraFOV*math.pi)/180.0)/2.0)
            totalDistance = int((totalDistance*100.0)/12.0)/100.0 + robot2camera # make into 2 decminal pt and ft
            return totalDistance 
            
        def fixDistance(x): # use polynomial fit from MATLAB to adjust for error and get more exact result
        	distance = (-2.9565*10**-6*x**3 + 0.0017*x**2 + 0.6935*x + 11.8683)/12 
        	distance = int(distance*100.0)/100.0
        	return distance
            
        def targetPixelWidth():
            w1 = Rect_coor[1][0] - Rect_coor[0][0]
            w2 = Rect_coor[2][0] - Rect_coor[3][0]
            width = (w1 + w2)/ 2.0
            return math.fabs(width)
        
        totalDistance_W = Distance(targetWidth, w, targetPixelWidth(), horizontal_cameraFOV)
        distance_horizontal = math.sqrt(totalDistance_W**2.0 - towerH**2.0)
        distance_final = int(fixDistance(distance_horizontal*12)*100.0)/100.0 
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        # check to make sure right number displayed
        self.image = cv2.putText(self.image,'Distance: ' + str(distance_final) + 'ft',(300,50), font, 0.5,(0,0,255),1,cv2.LINE_AA)
        
        return distance_final
        
        
       