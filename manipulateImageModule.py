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

def darkenImage(image, scale):
    darker = (image * scale).astype(np.uint8)
    return darker
    
def prioritizeTarget(contours):
    if len(contours) == 0:
        cnt = 0
        valid = False
    elif len(contours) == 1:
        cnt = contours[0]
        if len(contours[0]) >= 4:
            valid = True
        else:
            valid = False
    else:
        contours_revised = nlargest(2, contours, key=len)
        if len(contours_revised[0]) >= 4 and len(contours_revised[1]) >= 4:
            valid = True
            # Area of longest contour
            momentsL = cv2.moments(contours_revised[0])
            areaL = momentsL['m00']
            # Area of second longest contour
            momentsSL = cv2.moments(contours_revised[1])
            areaSL = momentsSL['m00']
            if areaL > areaSL:
                cnt = contours_revised[0]
            else:
                cnt = contours_revised[1]
        elif len(contours_revised[0]) <= 4 and len(contours_revised[1]) <= 4:
            cnt = 0
            valid = False
        elif len(contours_revised[0]) <= 4:
            cnt = contours_revised[1]
            valid = True
        else:
            cnt = contours_revised[0]
            valid = True
        
    return cnt, valid
    
        
def contours(img_orig, mask):
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt, valid = prioritizeTarget(contours)
    if valid:
        try:
            cv2.drawContours(img_orig, [cnt], -1, (255,0,0), 2)
        except:
            valid = False
    return cnt, contours, valid
        
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
    
    corners = cv2.goodFeaturesToTrack(corners_img, 4, 0.2, 10)
    corners = np.int0(corners)
    
    # Load original image and draw BFR and corners
    cv2.drawContours(img_orig, [box], 0, (0,0,255), 2)
    for i in corners:
        x,y = i.ravel()
        cv2.circle(img_orig, (x,y), 5, (255, 0, 255), -1)
    
    return hull, corners, img_orig
    

def drawCenterLine(BFR_img, cx,cy):
    h,w,c = BFR_img.shape
    cv2.line(BFR_img,(w/2, h/2), (cx, cy), (0,0,255), 3)
    return BFR_img

def dilateAndErode(img, size):
    kernel = np.ones((size,size), np.uint8)
    dilation = cv2.dilate(img,kernel,iterations=1)
    erosion = cv2.erode(dilation,kernel,iterations = 1)
    return erosion 

def isValid(hull, corners):
    match_quality = shapeMatch(hull)
    
    if len(corners) < 4 or match_quality > 0.16:
        return False
    else:
        return True 

def isValidAR(Rect_coor):
    w1 = Rect_coor[1][0] - Rect_coor[0][0]
    w2 = Rect_coor[2][0] - Rect_coor[3][0]
    w = (w1 + w2)/2.0
    
    h1 = Rect_coor[3][1] - Rect_coor[0][1]
    h2 = Rect_coor[2][1] - Rect_coor[1][1]
    h = (h1 + h2)/2.0
    
    aspect_ratio = float(w)/h
    
    # Real aspect ratio is 20"/12" = 1.666666 (used dimensions from target) 
    if aspect_ratio < 1.1 or aspect_ratio > 2.1:
        return False
    else:
        return True
    
    
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
    
def validStatus(BFR_img):
    font = cv2.FONT_HERSHEY_COMPLEX
    BFR_img = cv2.putText(BFR_img,'Valid Update: False',(10,50), font, 0.5,(0,0,255),1,cv2.LINE_AA)
    return BFR_img
        
    
   
    
    
        
        
        
