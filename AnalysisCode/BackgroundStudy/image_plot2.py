#! /usr/bin/env python
#
"""  This script will display some images already put into numpy foramt 

     Extra discription
     
     usage:  image_plot.py  [path to images to display]  
     
     
     
"""
import sys
import math
import numpy
import scipy
import scipy.ndimage
import scipy.ndimage.filters
import glob
import matplotlib.pyplot
#import matplotlib.backends.backend_pdf
import os
import Image

# get arguments
inputFiles=glob.glob(sys.argv[1])
for inputFile in inputFiles:
        pil_im=Image.open(inputFile)
        inputData_raw=numpy.array(pil_im.getdata()).reshape(pil_im.size[0], pil_im.size[1])
        inputData=scipy.ndimage.filters.gaussian_filter(inputData_raw, 0.5, order=0, output=None, mode='reflect', cval=0.0)# smear it
        
        boolArray=inputData > 100
        print " Number of pixels above background:",  numpy.sum(boolArray)
        print "Hottest pixel: ",numpy.amax(inputData)
        matplotlib.pyplot.gray()
        #matplotlib.pyplot.title("Data From "+fileRootName)
        #matplotlib.pyplot.imshow(boolArray)
        matplotlib.pyplot.imshow(inputData*boolArray,cmap=matplotlib.pyplot.cm.gray)
        matplotlib.pyplot.show()
        #data=numpy.reshape(inputArray,-1)  # need to format the numpyArray as a single dimension
        #matplotlib.pyplot.title("Data From "+fileRootName)
        #matplotlib.pyplot.yscale('log')
        raw_input("Press Enter To Continue")



# form list of npz files
# for each file
#    compute the average for all pixels for all images
#    compute the STD for all pixels for all images
#    print out the results 




