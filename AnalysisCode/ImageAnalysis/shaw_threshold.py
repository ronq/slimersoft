import numpy as np
from scipy import *
from scipy import ndimage

def get_threshold(data):
	mean = ndimage.mean(data)
	stdev = ndimage.standard_deviation(data)
	out = recursive_threshold(data,mean,stdev,0)
	return out

def recursive_threshold(data,mean,stdev,old):
	if (mean+4*stdev)==old:
		return [mean,stdev]
	else:
		bkg = data.copy()
		bkg[bkg>=(mean+4*stdev)]=0
		tmp = bkg[bkg!=0]
		new_mean = bkg.sum()/double(len(tmp))
		tmp = (tmp-new_mean)**2
		new_stdev = sqrt(tmp.sum()/double(len(tmp)))
		return recursive_threshold(data,new_mean,new_stdev,mean+4*stdev)
