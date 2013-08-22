"""
    Erik Shaw's Cluster Finding Code for SLIMER. Adopted from slimerAna2_mag10.py
"""
import Image
from shaw_threshold import *
#from skimage.filter import threshold_otsu
import sys
from ROOT import *
from pylab import *
from scipy import *
import numpy as np
from scipy import ndimage
from scipy import special
#import matplotlib.pyplot as plt	
from shaw_clusterAna2 import *
import os
import glob


#extract data from picture into numpy array
x_size = 512
y_size = 512
X = range(x_size)
Y = range(y_size)
size = x_size*y_size
Z = range(size)


averages = np.array([[av_h.GetBinContent(i+1,j+1) for i in X] for j in Y],dtype=np.float)
stdevs = np.array([[stdev_h.GetBinContent(i+1,j+1) for i in X] for j in Y],dtype=np.float)

# This is where the new code begins
# data = background subtracted dat

out = ndimage.gaussian_filter(data, 7)
threshold = get_threshold(out)

data -= threshold[0]+3*threshold[1]
out -= threshold[0]+3*threshold[1]
out[out<0] = 0




clusters = get_clusters(out,0.5*threshold[1])
for cluster in clusters:
	integral = 0
	count = 0
	smooth_integral = 0
	maximum = 0
	maximum_smooth = 0
	pixels = cluster.size
	for coord in cluster:
		smooth_integral+=out[coord[0]][coord[1]]
		if maximum < data[coord[0]][coord[1]]:
			maximum = data[coord[0]][coord[1]]
		if maximum_smooth < out[coord[0]][coord[1]]:
			maximum_smooth = out[coord[0]][coord[1]]
		if data[coord[0]][coord[1]]>0.5*threshold[1]:
			integral+=data[coord[0]][coord[1]]
			count+=1
	
