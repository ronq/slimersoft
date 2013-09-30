import numpy as np
from scipy import *
from scipy import ndimage

def findpeak(data,threshold):
	labeled, num_objects = ndimage.label(data>threshold)
	slices = ndimage.find_objects(labeled)
	return slices

