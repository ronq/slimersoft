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
	        # these are the output arrays
	        self.integrate_fit=[]
	        self.integrate_pixels=[]
	        self.peakh_fit=[]
	        self.peakh_pixels=[]
	        self.peaka_fit=[]
	        self.peaka_pixels=[]
	        self.raw_pixel_integral=[]
	        self.raw_pixel_area=[] 
	        self.threshold=[]
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
            
            self.integrate_fit.append(abs(2*pi*p[1]*p[5]*p[6]*percent*percent))
            self.integrate_pixels.append(smooth_integral)
            self.peakh_fit.append(p[1])
            self.peakh_pixels.append(out[int(p[3])][int(p[4])])
            self.peaka_fit.append(abs(pi*p[5]*p[6]))
            self.peaka_pixels.append(num_smooth_pix)
            self.raw_pixel_integral.append(integral)
            self.raw_pixel_area.append(num_pix) 
            self.threshold.append(threshold)
            # end new output code 
        return 
      #---------------------------------------------------------------------------
      #---------------------------------------------------------------------------
      def GenerateOutput(self):
            """ load relevant results into standard output variables
            """
            numPeaks = [len(self.threshold) for entry in self.threshold]     
            self.shawfitDict={
            'ShawFit_IntegratedFit':self.integrate_fit,
            'ShawFit_IntegratedPixels':self.integrate_pixels,
            'ShawFit_PeakHeightFit':self.peakh_fit,
            'ShawFit_PeakHeightPixels':self.peakh_pixels,
            'ShawFit_PeakAreaFit':self.peaka_fit,
            'ShawFit_PeakAreaPixels':self.peaka_pixels,
            'ShawFit_IntegratedRawPixels':self.raw_pixel_integral,
            'ShawFit_PeakAreaRawPixels':self.raw_pixel_area,
            'ShawFit_Threshold':self.threshold,
            'ShawFit_NumPeaks':numPeaks
            }
            return
      #---------------------------------------------------------------------------
      def DoIt(self,inputArray):
            #self.clusterOutput=cluster_output.cluster_output()
            self.imageArray=inputArray
            self.DoFit(self.imageArray)
            self.GenerateOutput() # load results into the final observables
            return    
      #------------------------------------------------------------------------------    
