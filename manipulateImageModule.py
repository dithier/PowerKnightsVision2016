# -*- coding: utf-8 -*-
"""
Created on Wed May 11 11:06:14 2016

@author: Ithier
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:37:06 2016

@author: Ithier
"""

import cv2
import numpy as np 
from heapq import nlargest
from imageCalculationsClass import organizeCorners 

minArea = 400

def darkenImage(image, scale):
    darker = (image * scale).astype(np.uint8)
    return darker
    
def contours(img_orig, mask):
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt, valid, Rect_coor, BFR_img, hull = prioritizeTarget(contours, img_orig) # select the best contour that could be a target
    if valid:
        try:
            cv2.drawContours(img_orig, [cnt], -1, (255,0,0), 2)
        except:
            valid = False
    return cnt, valid, Rect_coor, BFR_img, hull
        
def findCenter(cnt, image):
    M = cv2.moments(cnt)
    # FIND CENTROID
    #   Cx = M10/M00, Cy = M01/M00
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/ M['m00'])
    cv2.circle(image, (cx,cy), 8, (0, 255, 140), -1)
    return cx, cy
    
def bestFitRect(img_orig, cnt):
    # Find convex hull
    hull = cv2.convexHull(cnt)
    box = np.int0(hull)
    
    # Create black image, draw rectangle hull on it, corner detection
    corners_img = np.zeros((img_orig.shape[0],img_orig.shape[1],img_orig.shape[2]), np.uint8)
    cv2.drawContours(corners_img, [box], 0, (255,255,255), -1)
    corners_img = cv2.cvtColor(corners_img, cv2.COLOR_BGR2GRAY) 
    
    #                                 image, number of corners, quality (0-1), min euclidean dist
    corners = cv2.goodFeaturesToTrack(corners_img, 4, 0.2, 10) # Find coordinates for the four corners
    corners = np.int0(corners)
    
    # Load original image and draw BFR and corners
    cv2.drawContours(img_orig, [box], 0, (0,0,255), 2)
    for i in corners:
        x,y = i.ravel()
        cv2.circle(img_orig, (x,y), 5, (255, 0, 255), -1)
    
    return hull, corners, img_orig
    

def drawCenterLine(BFR_img, cx,cy):
    h,w,c = BFR_img.shape
    cv2.line(BFR_img,(w/2, h/2), (cx, cy), (0,0,255), 3) # draws line from center of camera image to center of target
    return BFR_img

def dilateAndErode(img, size):
    kernel = np.ones((size,size), np.uint8)
    dilation = cv2.dilate(img,kernel,iterations=1)
    erosion = cv2.erode(dilation,kernel,iterations = 1)
    return erosion 

# Determine if the hull (contour of the target) is a valid target 
def isValid(hull, corners):
    match_quality = shapeMatch(hull) # the closer match_quality is to zero the better the match
    
    if len(corners) < 4 or match_quality > 0.16: # make sure there are at least four corners and a reasonable match_quality
        return False
    else:
        return True 

# Check that the aspect ratio of the target is appropriate and thus whether it is a valid target
def isValidAR(Rect_coor):
    ''' Note on coordinate system: The top left corner of the target is Rect_coor[0], the top right is Rect_coor[1],
    the bottom right is Rect_coor[2], and the bottom left is Rect_coor[3]. The second index determines whether it is an
    x or y coordinate. Ex, Rect_coor[1][0] is the x value of the top right corner of the target while Rect_coor[1][1] is
    the y coordinate for the top right corner.
    '''
    w1 = Rect_coor[1][0] - Rect_coor[0][0]
    w2 = Rect_coor[2][0] - Rect_coor[3][0]
    w = (w1 + w2)/2.0 # average width of rectangle based on both sides
    
    h1 = Rect_coor[3][1] - Rect_coor[0][1]
    h2 = Rect_coor[2][1] - Rect_coor[1][1]
    h = (h1 + h2)/2.0 # average height of rectangle based on both sides
    
    aspect_ratio = float(w)/h
    
    # Real aspect ratio is 20"/12" = 1.666666 (used dimensions from target) 
    if aspect_ratio < 1.1 or aspect_ratio > 2.1:
        return False
    else:
        return True
    
# Determine how close the found target's contour is to the rectangle.png picture which was made based on target dimensions 
# from the game manual     
def shapeMatch(hull):
    '''
    Rectangle.png was created with this code
    cv2.rectangle(rectangle,(20,20),(120,80),(255,255,255),-1)  # coordinates chosen by making sure it has same aspect ratio as real life targe
    cv2.imwrite('rectangle.png', rectangle)
    '''
    # load image to compare 
    rectangle = cv2.imread('rectangle.png', 0)
    
    # Threshold and get contours
    ret, thresh = cv2.threshold(rectangle, 127, 255, cv2.THRESH_BINARY)
    img, contours, hierarchy = cv2.findContours(thresh,2,1)
    cnt = contours[0]
    match_quality = cv2.matchShapes(cnt,hull,1,0.0)
    
    return match_quality 

def zeroVariables():
    cnt = 0
    Rect_coor = 0
    BFR_img = 0
    hull = 0
    return cnt, Rect_coor, BFR_img, hull

# Choose target with largest area    
def prioritizeTarget(contours, img_orig):
    valid = False
    areas = []
    if len(contours) == 0: # no contours found
        cnt, Rect_coor, BFR_img, hull = zeroVariables()
    else:
        biggestContours = nlargest(20, contours, key=len) # take twenty longest contours
        
        # Determine area of each contour and sort by largest to smallest
        for i in range(0,len(biggestContours)):
            if len(biggestContours[i]) > 3:
                contourMoment = cv2.moments(biggestContours[i])
                contourArea = contourMoment['m00']
                if contourArea > minArea:
                    areas.append(contourArea) 
        areas = np.array(areas)
        area_indices = np.argsort(areas)
        
        if len(areas) > 0:
            # Check for validity of contours in order of largest area to smallest
            for i in reversed(area_indices):
                # Find BFR
                hull, corners, BFR_img = bestFitRect(img_orig, biggestContours[i])
                
                # Make sure there are 4 corners
                if len(corners) == 4:
                    Rect_coor = organizeCorners(corners)
                    # Check validity
                    validUpdate1 = isValidAR(Rect_coor)
                    validUpdate2 = isValid(hull, corners)
                    
                    # If this breaks then we have found our contour
                    if validUpdate1 == True and validUpdate2 == True:
                        valid = True
                        cnt = biggestContours[i]
                        break
                    
                    # Assign zeros if we've tried all contours and none succesful
                    if i == area_indices[0] and valid == False:
                        cnt, Rect_coor, BFR_img, hull = zeroVariables()
                        
                else:
                    cnt, Rect_coor, BFR_img, hull = zeroVariables()
        else:
            cnt, Rect_coor, BFR_img, hull = zeroVariables()
           
    return cnt, valid, Rect_coor, BFR_img, hull

   
    
    
        
        
        
