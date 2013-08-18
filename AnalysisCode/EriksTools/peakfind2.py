import numpy as np
from scipy import *
from scipy import ndimage

def findpeak(data,threshold):
	#data_max = ndimage.maximum_filter(data,neighborhood_size)
	#maxima = (data == data_max)
	#data_min = ndimage.minimum_filter(data,neighborhood_size)
	#diff = ((data_max-data_min) > threshold)
	#maxima[diff == 0] = 0
	labeled, num_objects = ndimage.label(data>threshold)
	slices = ndimage.find_objects(labeled)
	print slices
	return slices

