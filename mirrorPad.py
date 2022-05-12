#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 23:35:59 2021

Pads the image "Im" to retain its dimensions when filtered using "f".
The padding method is "mirror". Note that the 

@author: ruwwad
"""

def mirrorPad(Im, f):
    # Pads the image to retain its dimensions when filtered using "f".
    import numpy as np
    fr = f.shape[0]  #Number of rows in the filter
    fc = f.shape[1]  #Number of columns in the filter
    x = int(np.floor(fr/2))  #Offset in the x-axis
    y = int(np.floor(fc/2))  #Offset in the y-axis
    
    xi = Im.shape[0] - x - 1
    xf = 2*Im.shape[0] + x -1
    
    yi = Im.shape[1] - y - 1
    yf = 2*Im.shape[1] + y - 1
    
    ImCent = np.hstack((np.flip(Im[:,1:], axis=1), Im, np.flip(Im[:,:-1], axis=1)))
    ImPad = np.vstack((np.flip(ImCent[1:,:], axis=0), ImCent, np.flip(ImCent[:-1,:], axis=0)))
    
    # Padding the image depends on the dimensions of the filter, or rather,
    # whether they are even or odd. So you could have:
        # fr: odd,   fc: odd
        # fr: odd,   fc: even
        # fr: even,   fc: odd
        # fr: even,   fc: even
    # Each of these condition requires its own equation for finding the padded
    # image. Such conditions can be accounted for using if statements.

    #Check if the filter has odd dimensions
    if fr/2 != int(fr/2) and fc/2 != int(fc/2):
        Im_pad = ImPad[xi:xf, yi:yf]
    
    #Check if fr is odd while fc is even
    elif fr/2 != int(fr/2) and fc/2 == int(fc/2):
        Im_pad = ImPad[xi:xf, yi:yf-1]
    
    #Check if fr is even while fc is odd
    elif fr/2 == int(fr/2) and fc/2 != int(fc/2):
        Im_pad = ImPad[xi:xf-1, yi:yf]
    
    #Check if the filter has even dimensions
    else:
        Im_pad = ImPad[xi:xf-1, yi:yf-1]
    
    return Im_pad