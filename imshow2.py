#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 02:50:28 2021

I have written this function to make it much quicker to show high quality
figures. Plus, it does somethings that I prefer. For example, cmap='gray' is 
automatically applied to grayscale images. Another example is when I use
cmap ='gray', this automatically normalizes the image which I find to be
annoying sometimes, so this function gets rid of that. Also, it removes the
useless axis shown in the image, etc.

Next, I plan on improving it so that it accepts N number of images and titles,
and then use subplots to show them, and depending on that number, the figure
size will be chosen accordingly. This should not be difficult to implement,
and it will drastically increase the convenience of this function.

I have implemented the above, but it is still experimental

@author: ruwwad
"""

def imshow2(I, title='', grid=(1,1), subplot=(1)):
    import numpy as np
    import matplotlib.pyplot as plt
    # from normIm import normIm
    normIm = lambda Im,L,H: (Im-Im.min()) / (Im.max()-Im.min()) * (H-L)+L
    plt.figure(dpi=300, figsize=(5.5*grid[1],5.5*grid[0]))
    if type(I) == type(np.arange(1)):
        I = [I]  #Fixes the below for loop
    
    for i, Im in enumerate(I):
        plt.subplot(grid[0],grid[1], subplot[i])
        plt.axis('off')
        try:
            plt.title(title[i])
        except:
            print('The number of titles is less than the number of image!')
        
        Im = np.array(Im, dtype=float)  #To make sure the image is of type float
        n = int(np.ceil(np.log2(1+np.amax(np.array(Im))
                                - np.amin(np.array(Im)))))  #Number of bits required to represent x
        # n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
        L = 2**n  #Number of intensity levels available in the image (in other words, it is our bandwidth)
        minimum = np.amin(Im)
        
        #If the image has the channels in the first axis, then move it to the last
        if len(Im.shape) == 3 and min(Im.shape) == Im.shape[0]:
            print('Moved the channels axis to align with plt.imshow')
            Im = np.moveaxis(Im, 0, 2)
        # The below lines are implemented later
        # elif len(Im.shape) == 4 and min(Im.shape[1:]) == Im.shape[1]:
        #     print('Im.shape =', Im.shape)
        #     Im = np.moveaxis(Im, 1, 3)
        #     print('Im.shape =', Im.shape)
        if len(Im.shape) == 2 or (len(Im.shape) == 3 and Im.shape[2] == 1): #If the image was grayscale,
            if L == 256 and (minimum >= 0):
                plt.imshow(np.uint8(Im), 'gray', vmin=0, vmax=255)
            elif L==1 and (minimum >= 0):
                plt.imshow(np.uint8(Im*255), 'gray', vmin=0, vmax=255)
            else:
                plt.imshow(normIm(Im, 0, 255), 'gray', vmin=0, vmax=255)
                print("The image does NOT have a standard range... \nNormalizing...")
        elif len(Im.shape) == 3: #If the image was RGB,
            if L == 256 and (minimum >= 0):
                plt.imshow(np.uint8(Im), vmin=0, vmax=255)
            elif L==1 and (minimum >= 0):
                plt.imshow(np.uint8(Im*255), vmin=0, vmax=255)
            else:
                print("The image does NOT have a standard range... \nNormalizing...")
                plt.imshow(normIm(Im, 0, 1), vmin=0, vmax=255)
        
        elif len(Im.shape) == 4:  #If the image was a tensor (most likely)
            # Im = Im.cpu().detach().numpy()[0]
            Im = np.moveaxis(Im[0],0,-1)
            if Im.shape[-1] == 1: #If the image was grayscale,
                if L == 256 and (minimum >= 0):
                    plt.imshow(np.uint8(Im), 'gray', vmin=0, vmax=255)
                elif L==1 and (minimum >= 0):
                    plt.imshow(np.uint8(Im*255), 'gray', vmin=0, vmax=255)
                else:
                    print("The image does NOT have a standard range... \nNormalizing...")
                    plt.imshow(normIm(Im, 0, 255), 'gray', vmin=0, vmax=255)
            elif Im.shape[-1] == 3: #If the image was RGB,
                if L == 256 and (minimum >= 0):
                    plt.imshow(np.uint8(Im), vmin=0, vmax=255)
                elif L==1 and (minimum >= 0):
                    plt.imshow(np.uint8(Im*255), vmin=0, vmax=255)
                else:
                    print("The image does NOT have a standard range... \nNormalizing...")
                    plt.imshow(normIm(Im, 0, 255), vmin=0, vmax=255)
        else:
            print("Something isn't right with the dimensions of the image, so fix it!")
            #The above line is problematic