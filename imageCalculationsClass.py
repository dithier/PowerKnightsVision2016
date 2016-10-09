# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 17:03:57 2016

@author: Ithier
"""
import cv2 
import math 
from collections import Counter


# Take corner coordinates and organize them in a specific order for easier computations later  
# This is necessary because the corners are returned in a different order each time they are determined
def organizeCorners(corners):
    
    # Save coordinates to variable Rect_coor where corner 0 is the top left corner and the rest are numbered clockwise
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
        
    # Determine x coordinates
    corners2 = list(corners.ravel())
    x = []
            
    for i in xrange(0, len(corners2), 2):
        x.append(corners2[i])
        
    ''' There are three different cases that need to be considered: 1) There are no repeats in the x coordinates
    meaning that you may have an array like [100, 200, 105, 202]  2) There is one repeat in the x coordinates such as
    [100, 100, 200, 202]  3) There are two repeats in the x coordinates such as [100, 200, 100, 200]. The number of 
    duplicates determines the methods to be used to determine the order of the coordinates. This is done below
    '''
    # Check for duplicate and find value
    duplicate = len(x) != len(set(x)) # returns True of False on whether there is a duplicate in the x array
    c = Counter(x).items() # gives array listing the numbers in the array and how many times they occur
    doubleVal = [] # this list keeps track of the VALUES of the x coordinates that are repeated. It will be empty if there are no repeats
    if len(c) == 2: # there are two repeats in the x coordinates
        doubleVal.append(c[0][0])
        doubleVal.append(c[1][0])
        doubleVal.sort()
    elif len(c) == 3: # there is one repeat in the x coordinates
        for i in range(0,len(c)):
            if c[i][1] == 2:
                doubleVal.append(c[i][0])
                break
    
    # Determine if repeat number is max or min in array (ie whether it is a top left or right corner (max) or
    # whether it is a bottom left or right corner (min))
    if len(doubleVal) > 0:
        maximum = max(x) == doubleVal[0] # returns True if it is a maximum (a top corner) or False if it isn't (meaning it is a bottom corner)
        
    # Find top right and bottom right coordinates
    #     find the indices for the two right corners
    if duplicate: # if duplicate exists
        if len(doubleVal) == 1: # if there is one duplicate
            if maximum: # the duplicate is of a top corner
                indices = [i for i, a in enumerate(x) if a == doubleVal[0]]
                maxXind = indices[0]
                secMaxXind = indices[1]
            else: # the duplicate is of a bottom corner
                maxXind = x.index(max(x))
                copy = x[:]
                copy.pop(maxXind)
                secMaxVal = max(copy)
                secMaxXind = x.index(secMaxVal)
        else: # there are two duplicates
            indices = [i for i, a in enumerate(x) if a == doubleVal[1]]
            maxXind = indices[0]
            secMaxXind = indices[1]
    else: # there are not duplicates
        maxXind = x.index(max(x))
        copy = x[:]
        copy.pop(maxXind)
        secMaxVal = max(copy)
        secMaxXind = x.index(secMaxVal)
        
    #     determine which index is top and by default is bottom by looking at corresponding 
    # y values to the x coordinates 
    # based on OpenCV coordinate system, top left of pic is (0,0) and x increases as it moves left and y increases as you move down
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
        
    
def findAngle(image, cx):
    global horizontal_cameraFOV, vertical_cameraFOV 
    global h,w,c
    global font
    horizontal_cameraFOV = 47.0
    vertical_cameraFOV = 36.5
    
    h, w, c = image.shape # h = height, w = width, c = channel
    offsetpx = (w/2.0) - cx # offset from center of camera image to center of target (pixels)
    
    angle= int(horizontal_cameraFOV * (offsetpx / w)*100.0)/100.0 
    
    font = cv2.FONT_HERSHEY_COMPLEX
    image = cv2.putText(image,'Angle: ' + str(angle),(90,50), font, 1,(0,0,255),2,cv2.LINE_AA)

    return angle
    
def findDistance(image, Rect_coor):
    towerH = (89/12) # height from ground to center of target (in real life) in ft
    
    # dimensions from target (from game manual)
    targetWidth = 20.0 # in
    
    robot2camera = 1.5 # ft    distance from front of robot to camera (so that distance calculation is distance from tower to front of robot)
    
    def Distance(targetActual, imagePx, targetPx, cameraFOV):
        totalDistance = (((targetActual*imagePx)/targetPx)/2.0) / \
    			math.tan(((cameraFOV*math.pi)/180.0)/2.0)
        totalDistance = int((totalDistance*100.0)/12.0)/100.0  # make into 2 decminal pt and ft
        return totalDistance 
        
    def fixDistance(x): # use polynomial fit from MATLAB to adjust for error and get more exact result
    	distance = (-2.9565*10**-6*x**3 + 0.0017*x**2 + 0.6935*x + 11.8683)/12 
    	distance = int(distance*100.0)/100.0
    	return distance
        
    def targetPixelWidth():
        w1 = Rect_coor[1][0] - Rect_coor[0][0]
        w2 = Rect_coor[2][0] - Rect_coor[3][0]
        width = (w1 + w2)/ 2.0 # average width of target 
        return math.fabs(width)
    
    totalDistance_W = Distance(targetWidth, w, targetPixelWidth(), horizontal_cameraFOV) # diagonal distance from camera to tower
    try:
        distance_horizontal = math.sqrt(totalDistance_W**2.0 - towerH**2.0) + robot2camera # horizontal distance from front of robot to tower
        distance_final = int(fixDistance(distance_horizontal*12)*100.0)/100.0 
    except:
        distance_final = totalDistance_W
        print 'May be error with distance calculation'
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    # check to make sure right number displayed
    image = cv2.putText(image,'Distance: ' + str(distance_final) + 'ft',(90,280), font, 1,(0,0,255),2,cv2.LINE_AA)
    
    return distance_final
    
    
   