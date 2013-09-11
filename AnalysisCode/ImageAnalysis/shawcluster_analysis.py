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
        # these are the output arrays
        self.cluster_integral=[]
        self.cluster_pixels=[]
        self.cluster_smooth_integral=[]
        self.cluster_smooth_pixels=[]
        self.cluster_max=[]
        self.cluster_smooth_max=[]
        self.threshold=[]
        self.threshold_mean=[]
        self.foundClusters=False
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
            self.cluster_integral.append(integral)
            self.cluster_pixels.append(count)
            self.cluster_smooth_integral.append(smooth_integral)
            self.cluster_smooth_pixels.append(pixels)
            self.cluster_max.append(maximum)
            self.cluster_smooth_max.append(maximum_smooth)
            self.threshold.append(threshold[1])   
            self.threshold_mean.append(threshold[0])         
        return  	  
		
	
		 
	  #---------------------------------------------------------------------------
      def GenerateOutput(self):
            """ load relevant results into standard output variables
            """
            numPeaks = [len(self.threshold) for entry in self.threshold]  
            self.foundClusters=len(self.threshold)>0   
            self.shawclusterDict={
            #'ShawCluster_IntegratedRawPixels':self.cluster_integral,
            #'ShawCluster_ClusterRawArea':self.cluster_pixels ,
            #'ShawCluster_IntegratedPixels':self.cluster_smooth_integral,
            #'ShawCluster_ClusterArea':self.cluster_smooth_pixels,
            #'ShawCluster_PeakHeightRaw':self.cluster_max ,
            #'ShawCluster_PeakHeight':self.cluster_smooth_max,
            #'ShawCluster_Threshold':self.threshold,
            #'ShawCluster_ThresholdMean':self.threshold_mean,
            'ShawCluster_NumPeaks':numPeaks
            }
            return
	  #---------------------------------------------------------------------------
      def DoIt(self,inputArray):
            self.imageArray=inputArray
            self.DoCluster(self.imageArray)
            self.GenerateOutput() # load results into the final observables
            return    
      #------------------------------------------------------------------------------   
