# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 20:54:38 2022

@author: ruwwad
"""

def hist_adv(Im):
    import numpy as np
    # Finds the histogram of the image
    # This function has assumption:
    # - All intensity values are integers
    
    Im = np.array(Im)  #Converts the image into a numpy array to avoid edge-cases
    # The if statement below allow the function to find the histogram of:
    # 1- greyscale images.
    # 2- RGB images.
    # 3- Videos of rgb images.  <-- The implementation here is WRONG!
    if len(Im.shape) == 1:
        Im = np.array([[[Im]]])
    elif len(Im.shape) == 2:
        Im = np.array([[Im]])
    elif len(Im.shape) == 3:
        Im = np.array([Im])
    n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent Im
    h = np.zeros(2**n)  #Initializes the histogram
    for i in range(Im.shape[0]):
        for j in range(Im.shape[1]):
            for k in range(Im.shape[2]):
                for n in range(Im.shape[3]):
                    h[int(Im[i,j,k,n])] += 1
    
    histo = np.empty((2,0))  #Intialization
    for i in range(h.shape[0]):
        if h[i] != 0:
            histo = np.hstack((histo, [[h[i]],[i]]))
    return np.array(histo, dtype=int)