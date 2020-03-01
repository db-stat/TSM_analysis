#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: divya
"""

from __future__ import print_function

import os
import numpy as np
from glob import glob
import matplotlib.pyplot as plt


Study = 'Cambridge'
DesignFile = 'OneSampleTtest_GroupSize20'
Smoothing = '4mm'
Design = 'boxcar30'
parcels = 208

wdir = '/home/Divya/analysis'   
rdir = '/home/Divya/analysis/FSL/Results'
output_dir = os.path.join(wdir, 'TSM/outputs', Study+'_'+DesignFile+'_values', Smoothing+'_'+Design, 'F_test_100run')

axis2 = sorted([os.path.basename(x) for x in glob(os.path.join(output_dir, 'p', 'p_10*'))])  #len([os.path.basename(x) for x in glob(os.path.join(output_dir, 'p', 'p_[1-9]*'))])
print('length of Axis 2: ', len(axis2))

p_val = np.zeros((parcels, len(axis2)))
temp = np.zeros(parcels)   
y = 0
for j in axis2:     #range(0, axis2)
    data_file = os.path.join(output_dir, 'p', j)  
    temp = np.loadtxt(data_file, delimiter='\t')  
    for i in range(0, parcels):
      p_val[i,y] = temp[i]
    y+= 1


#-----------Which parcels?---------------------------------------
#count instances of p < 0.00024 for each parcel, i.e., along axis 2

sig_p = np.zeros((parcels, len(axis2)))
count_p = np.zeros(parcels)
for k in range(0, parcels):
    sig_p[k,:] = p_val[k,:]< 0.00024
    count_p[k] = sig_p[k,:].sum()


select = (count_p > 500)
false_pos = np.where(select)

print('List of significant(false positive) parcels for '+Smoothing+'_'+Design+': ' + str(np.where(select)))
print('No. of parcels with false positives: ' + str(len(false_pos[0])))  #output is a tuple : array([,,,], )  
rg_comp = 10000
percent = 100 * np.divide(count_p, rg_comp)


#histogram of uncorrected p-values of selected parcels

p_hist = np.zeros((16, len(axis2)))
t_hist = np.zeros((16, len(axis2)))
z = 0 
for j in axis2:
    data_file = os.path.join(output_dir, 'p', j)  
    temp = np.loadtxt(data_file, delimiter='\t')   
    for i in range(0, 16):               
      p_hist[i,z] = temp[i]
    z += 1

n_bins = 112 
fig, axs = plt.subplots(4, 4, sharey=True, tight_layout=True) 
k = 0 
for i in range(0, 4):
   for j in range (0,4):
      l = k+i+j             
      axs[i,j].hist(p_hist[l,0:len(axis2)], bins=n_bins)
     
   k += j
#   print(k)

plt.show()










    
    

