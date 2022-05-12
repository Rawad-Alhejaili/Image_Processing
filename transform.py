#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 17:57:07 2022

Applies a transformation map to an image

@author: ruwwad
"""

import numpy as np
def transform(Im, tx):
    Im = np.array(Im)
    #Number of bits required to represent Im and tx respectively.
    n = int(np.ceil(np.log2(np.amax(np.array(Im))-np.amin(np.array(Im))+1)))
    nTx = int(np.ceil(np.log2(tx.shape[0])))
    indices = np.hstack((2**(n-nTx) * (np.arange(tx.shape[0])), 2**n-1))
    if tx.shape[0] < 2**n:
        tx = np.hstack((tx, 2**n-1))
        # print(np.vstack((tx, indices)))
        newTx = np.zeros(2**n)
        for i, v in enumerate(tx[:-1]):
            j = indices
            m = (tx[i+1] - tx[i]) / (j[i+1] - j[i])  #slope
            b = v - m*j[i]  #offset
            for k in range(j[i], j[i+1]+1):
                newTx[k] = m*k + b
        tx = newTx
        # import matplotlib.pyplot as plt
        # plt.plot(tx)
    
    output = np.zeros(Im.shape)  #Preallocation
    for i in range(Im.shape[0]):
        for j in range(Im.shape[1]):
            output[i,j] = tx[int(Im[i,j])]
    return output

#Number of bits required to represent Im and tx respectively.
# tx = np.array([  0, 4, 4, 6])
# n = 4
# nTx = int(np.ceil(np.log2(tx.shape[0])))
# indices = np.hstack((2**(n-nTx) * (np.arange(tx.shape[0])), 2**n-1))
# if tx.shape[0] < 2**n:
#     tx = np.hstack((tx, 2**n-1))
#     # print(np.vstack((tx, indices)))
#     newTx = np.zeros(2**n)
#     for i, v in enumerate(tx[:-1]):
#         j = indices
#         m = (tx[i+1] - tx[i]) / (j[i+1] - j[i])  #slope
#         b = v - m*j[i]  #offset
#         for k in range(j[i], j[i+1]+1):
#             newTx[k] = m*k + b
#     tx = newTx