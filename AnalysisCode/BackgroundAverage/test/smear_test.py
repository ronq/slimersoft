#! /usr/bin/env python
#
"""  This script creates an image with a single pixel spike, then applies a guassian smear

     Extra text
     
     usage: smear_test.py
     
     
     
"""
import sys

import math
import numpy
import scipy
import scipy.ndimage
import Image
import matplotlib.pyplot


# create an 512x512 16 bit int array of zeros
imageArray=numpy.zeros( (512,512),dtype=numpy.uint16)
imageArray[256,100]=10000 # set 256, 256 equal to a very large value
imageArray[256,400]=22000
newArray_10=scipy.ndimage.filters.gaussian_filter(imageArray, 10.0, order=0, output=None, mode='reflect', cval=0.0)# smear it
newArray_50=scipy.ndimage.filters.gaussian_filter(imageArray, 50.0, order=0, output=None, mode='reflect', cval=0.0)# smear it
newArray_median=scipy.ndimage.filters.median_filter(imageArray, size=3, footprint=None, output=None, mode='reflect', cval=0.0, origin=0)

print "sum: ", newArray_median.sum()
matplotlib.pyplot.imshow((newArray_median>10), cmap=matplotlib.pyplot.cm.gray)  # for debugging
matplotlib.pyplot.show()


# plot it


