# -*- coding: utf-8 -*-
"""
Created on Tue May 17 23:52:34 2016

@author: Ithier
"""

def sendValues(sd, Angle, Distance, validCount, Locked):  
    sd.putNumber('Angle', Angle)
    sd.putNumber('Distance', Distance)
    sd.putNumber('validCount', validCount)
    sd.putBoolean('Locked', Locked)
    
    