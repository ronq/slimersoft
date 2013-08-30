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
#==================================================================================
class shawfit_analysis:
      """ this class performs Erik Shaw's Bivariate Gaussian fit to a greyscale image array

      """
      #------------------------------------------------------------------------------------------------------------------------------------------
      def __init__(self):
	  
	        return
	  #----------------------------------------------------------------------------
      def DoDBSCAN(self,minimumPoints,eps):
            self.db=dbscan_implementation(self.imageArray,minimumPoints,eps)
            return
      #---------------------------------------------------------------------------
      def DoFit(self,data):



        #extract data from picture into numpy array
        x_size = 512
        y_size = 512
        two_sigma_val = 0.0215392793
        X = range(x_size)
        Y = range(y_size)
        size = x_size*y_size
        Z = range(size)

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
        return coords, integral, smooth_integral, <count>, <pixels>, <maximum>, <maximum_smooth>, <data.max()>, <threshold[1]>
        p=(0,height,0,x,y,width_x,width_y)
        h1.Fill(abs(2*pi*p[1]*p[5]*p[6]*percent*percent))
	    h2.Fill(smooth_integral)
	    h3.Fill(p[1])
	    h4.Fill(out[int(p[3])][int(p[4])])
	    h5.Fill(abs(pi*p[5]*p[6]))
	    h6.Fill(num_smooth_pix)
	    h7.Fill(integral)
	    h8.Fill(num_pix)

        #---------------------------------------------------------------------------
      #---------------------------------------------------------------------------
        def GenerateOutput(self):
            """ load relevant results into standard output variables
            """
            # cluster energy
            # cluster "size" in units of pixels
            # cluster position
            # "energy density" of cluster
            # ratio of cluster counts to overall 
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
            self.DoFit(self.imageArray)
            self.GenerateOutput() # load results into the final observables
            return    
      #------------------------------------------------------------------------------    
