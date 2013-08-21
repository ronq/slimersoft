from shaw_peakfind2 import *
import numpy as np
#import sys
from scipy import *
from scipy import ndimage

def get_clusters(data,threshold):
	slices=findpeak(data,threshold)
	#in_cluster=data>threshold
	clusters=[]
	for s in slices:
		x = (s[0].start+s[0].stop-1)/2
		y = (s[1].start+s[1].stop-1)/2
		area = (s[0].stop-s[0].start)*(s[1].stop-s[1].start)
		data_of_interest = data[s[0].start:s[0].stop+1,s[1].start:s[1].stop+1]
		in_cluster = data_of_interest > threshold
		if area>10:
			#sys.setrecursionlimit(5000)
			#cluster=recursiveClusterDef(in_cluster,x,y)
			out = np.argwhere(in_cluster)
			out += [s[0].start, s[1].start]
			tmp = out.copy()
			too_much = np.argwhere(tmp==511)
			too_little = np.argwhere(tmp==0)
			#to_be_removed = [-1,-1]
			#other_rows = (out != to_be_removed).any(axis=1)
			#out_other_rows = out[other_rows]
			#bad = [-2,-2]
			if (out.size/2>100) and (out.size/2<25000) and len(too_much)==0 and len(too_little)==0:
				clusters.append(out)
	return clusters

