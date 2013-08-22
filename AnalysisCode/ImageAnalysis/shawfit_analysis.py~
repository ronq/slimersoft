"""
    Erik Shaw's Bivariate Gaussian Fit code for SLIMER. Adopted from slimerAna.py 
    
    May need to pull in /proj3/Slimer/Slimer_mk2/EriksCodeAndRootFiles/calculations.py
"""
import Image
from shaw_threshold import *
import sys
from ROOT import *
from pylab import *
from scipy import *
import numpy as np
from scipy import ndimage
from scipy import special
import matplotlib.pyplot as plt	
from shaw_fit import *
# perhaps not used
#from calculations import *
import os
import glob


#extract data from picture into numpy array
x_size = 512
y_size = 512
two_sigma_val = 0.0215392793
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
out -= threshold[0]+3*threshold[1]
data -= threshold[0]+3*threshold[1]
out[out<0] = 0


percent = special.erf(sqrt(2))
params = fitgaussian(out,0.5*threshold[1])
for p in params:
	fit = gaussian(*p)
	results = np.array([[fit(j,i) for i in X] for j in Y],dtype=np.float)
	coords = np.argwhere((results-p[0])/p[1]>two_sigma_val/(p[5]*p[6]))
	integral = 0
	smooth_integral = 0
	num_pix = 0
	num_smooth_pix = len(coords)
	for coord in coords:
		smooth_integral += out[coord[0]][coord[1]]
		if data[coord[0]][coord[1]]>0.5*threshold[1]:
			integral += data[coord[0]][coord[1]]
			num_pix += 1
bkgfile.Close()

