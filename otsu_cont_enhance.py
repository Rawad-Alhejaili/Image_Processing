# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 20:30:27 2022

@author: ruwwad
"""
import numpy as np
# from hist import hist
from hist_adv import hist_adv as hist
from otsuM import otsuM

def otsuHist(hist):
    # This function uses Otsu's method to perform automatic thresholding
    # The algorithm is based on the equations found on the wiki
    # Source: https://en.wikipedia.org/wiki/Otsu%27s_method
    import numpy as np
    
    histo = np.copy(hist)  #Histogram of the image
    histIm = histo[0,:]  #Frequency of each intensity value
    p = histIm/np.sum(histIm)  # PDF of the histogram
    
    # Preallocation
    # w0 is the probability of all dark intensities
    # w1 is the probability of all bright intensities
    # u0 is the mean value of dark intensities
    # u1 is the mean value of bright intensities
    # v is the intra-class variance
    # r is the intensity values in the image
    # vDict is used to find the threshold that results in the maximum
    # intra-class variance. The keys are the intra-class variance, while the
    # values are the thresholds.
    if histIm.shape[0] <= 2:
        print('\nhisto is equal to:\n{}'.format(histo))
        return histo[1,-1]
        # print('Success! The histogram is empty')
        # print(hist)
        # print(histIm)
        
    w0 = np.zeros(histIm.shape[0]-1); w1 = np.zeros(histIm.shape[0]-1)
    u0 = np.zeros(histIm.shape[0]-1); u1 = np.zeros(histIm.shape[0]-1)
    v = np.zeros(histIm.shape[0]-1); r = np.array(histo[1,:], dtype=int)
    vDict = {}
    for i in range(histIm.shape[0]-1):
        w0[i] = np.sum(p[:i+1])
        if w0[i] != 0:
            u0[i] = np.sum(r[:i+1] * p[:i+1]) / w0[i]
        else:
            u0[i] = 0
        
        w1[i] = np.sum(p[i+1:])
        if w1[i] != 0:
            u1[i] = np.sum(r[i+1:] * p[i+1:]) / w1[i]
        else:
            u1[i] = 0
        
        v[i]  = w0[i]*w1[i]*np.square(u0[i]-u1[i])
        vDict[v[i]] = np.append(vDict.get(v[i], np.array([], dtype=int)), np.array(r[i]+1))
        # The append function is used to avoid edge-cases.
        # If two thresholds resulted in the same intra class-variance,
        # the first threshold would be overwritten. This can be avoided by
        # storing the threshold values as arrays, and then append them
        # whenever a threshold results in the same intra-class variance.
        # Hence, multiple thresholds will can now be stored.
        # Highly unlikely that this will ever happen though.
        
        
    # The if statement below helps to alert the user of multiple thresholds
    # holding the same intra-class variance.
    try:
        if vDict[np.amax(v)].shape[0] == 1:
            return vDict[np.amax(v)][0]
        else:
            print("WARNING: There are two or more thresholds with the same intra-class variance!")
            print("         The returned value is a numpy array. Use indexing to choose")
            print("         the preferred threshold.")
            return vDict[np.amax(v)][np.round(vDict[np.amax(v)].shape[0])]
    except:
        print('Exception handled!')
        return r[0]
       
def something(Im_Histogram, otsus_histograms):
    t = np.zeros(len(otsus_histograms), dtype=int)
    histos = []
    for i,h in enumerate(otsus_histograms):
        t[i] = otsuHist(h)  #Threshold found using otsu's method
        h0 = Im_Histogram[:, np.amin(h[1,:]) : t[i]]  #Lower-side histogram
        h1 = Im_Histogram[:, t[i] : np.amax(h[1,:]) + 1] #Upper-side histogram
        # Please check the effectiveness of the if statement below.
        # It could negatively affect the results.
        if h.shape[1] <= 2:
            # h1 = Im_Histogram[:, t[i]-1 : np.amax(h[1,:]) + 1] #Upper-side histogram
            print('Success! h is equal to 1')
            print(h)
            print(h.shape)
        if h0.shape[1] < 2:
            h0 = Im_Histogram[:, np.amin(h[1,:]) : t[i]+1]  #Lower-side histogram
            print('Success! h0 is equal to 1')
            print(h0)
        if h1.shape[1] < 2:
            h1 = Im_Histogram[:, t[i]-1 : np.amax(h[1,:]) + 1] #Upper-side histogram
            print('Success! h1 is equal to 1')
            print(h1)
        
        histos.append(h0)
        histos.append(h1)
        # histos.append([h0, h1])
    return (t, histos)

def otsu_cont_enhance(Im, n):
    
    #Find the number of bits required to represent Im
    nMax = int(np.ceil(np.log2(np.amax(np.array(Im))-np.amin(np.array(Im))+1)))
    
    #If the user enters a value of n that exceeds the maximum possible value:
    if n > nMax:
        n = nMax
    
    # h = []
    # h = h.append(hist(Im))
    t = np.empty(0, dtype=int)  #Preallocating the thresholds
    tLSB = int(np.amin(Im))  #This is not necessarily the "LSB", but it is the zero state
    tMSB = otsuM(Im)  # t = 4
    t = np.append(t, [tLSB, tMSB])
    
    h = hist(Im)  #Image histogram
    histos = [[]]
    h0 = h[:, tLSB : tMSB]       # Lower-side histogram (from 0 to 3)
    h1 = h[:, tMSB : int(np.amax(Im)) + 1]   # Upper-side histogram (from 4 to 7)
    histos[0].append(h0)
    histos[0].append(h1)
    
    for i in range(n-1):
        # print(i)
        t_tmp, histo_tmp = something(h, histos[i])
        t = np.hstack((t, t_tmp))
        histos.append(histo_tmp)
        # print(np.sort(t))
    t = np.sort(t)
    return t

def unOtsu(Im, n, a):
    from transform import transform
    Im = np.array(Im)
    t = otsu_cont_enhance(Im, n)
    otsuIm = transform(Im, t)
    unOtsuIm = otsuIm+a*(Im-otsuIm)
    return unOtsuIm

# #Example
# Im = np.array([0, 1, 2, 3, 4, 5, 6, 7])
# # h = []
# # h = h.append(hist(Im))

# t000 = np.amin(Im)
# t100 = otsuM(Im)  # t = 4

# h = hist(Im)
# print(h)
# print(t100)
# h0 = h[:, np.amin(Im) : t100]       # 0 -- 3
# h1 = h[:, t100 : np.amax(Im) + 1]   # 4 -- 7

# t010 = otsuHist(h0)  # t010 = 2
# t110 = otsuHist(h1)  # t110 = 6


# h00 = h[:, np.amin(h0[1,:]) : t010]         # 0 -- 1
# h01 = h[:, t010 : np.amax(h0[1,:]) + 1]     # 2 -- 3
# h10 = h[:, np.amin(h1[1,:]) : t110]         # 4 -- 5
# h11 = h[:, t110 : np.amax(h1[1,:]) + 1]     # 6 -- 7

# print('otsuHist(h00) = {}'.format(otsuHist(h00)))
# print('otsuHist(h01) = {}'.format(otsuHist(h01)))
# print('otsuHist(h10) = {}'.format(otsuHist(h10)))
# print('otsuHist(h11) = {}'.format(otsuHist(h11)))


# t001 = otsuHist(h00)  # t001 = 1
# t011 = otsuHist(h01)  # t011 = 3
# t101 = otsuHist(h10)  # t101 = 5
# t111 = otsuHist(h11)  # t111 = 7






























