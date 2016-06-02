# -*- coding: utf-8 -*-
"""
Created on Tue May 17 23:52:34 2016

@author: Ithier
"""

def sendValues(sd, Angle, Distance, validUpdate, Locked):  
    sd.putNumber('Angle', Angle)
    sd.putNumber('Distance', Distance)
    sd.putBoolean('validUpdate', validUpdate)
    sd.putBoolean('Locked', Locked)
    
    