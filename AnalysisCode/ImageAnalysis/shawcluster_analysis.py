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
#==================================================================================
class shawcluster_analysis:
    """ this class performs Erik Shaw's Clustering to a greyscale image array

    """
      #------------------------------------------------------------------------------------------------------------------------------------------
      def __init__(self):
	  
	        return
      #---------------------------------------------------------------------------
      def DoCluster(self,data):

        #extract data from picture into numpy array
        x_size = 512
        y_size = 512
        X = range(x_size)
        Y = range(y_size)
        size = x_size*y_size
        Z = range(size)


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
		return coord, integral, smooth_integral, count, pixels, maximum, maximum_smooth, data.max(), threshold[1] 	   
	  #---------------------------------------------------------------------------
      def GenerateOutput(self):
            """ load relevant results into standard output variables
            """
            
            
            # may want to use different output variables for this
            
            self.clusterOutput.outputClusterSize=self.clusterPixels[self.bestClusterID]
            self.clusterOutput.outputCounts=self.clusterCounts[self.bestClusterID]
            self.clusterOutput.outputClusterFrac=self.clusterFrac[self.bestClusterID]
            self.clusterOutput.outputAvgPixelCount=self.avgPixelCount[self.bestClusterID]
            self.clusterOutput.outputPosition=self.clusterPosition[self.bestClusterID]
            self.clusterOutput.outputPositionVariance=self.clusterPositionVariance[self.bestClusterID]
            self.clusterOutput.outputPeakHeight=self.clusterHottestPixel[self.bestClusterID]
            self.clusterOutput.outputNumberOfClusters=float(self.maxClusterID)
            return
	  #---------------------------------------------------------------------------
      def DoIt(self):
            self.clusterOutput=cluster_output.cluster_output()
            self.imageArray=inputArray
            self.clusterPosition,  = self.DoCluster(self.imageArray)
            self.GenerateOutput() # load results into the final observables
            return    
      #------------------------------------------------------------------------------   
