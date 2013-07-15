#! /usr/bin/env python
#
"""  This script will analyze Numpy array formatted images to compare the averages of a couple of data sets 

     Extra discription
     
     usage:  background_average.py  [path to images to average] 
     
     
     
"""
import sys
import math
import numpy
import scipy
import glob




# get arguments
inputList=glob.glob(sys.argv[1])
for npzfile in inputList:
    inputArray=(numpy.load(npzfile))['imageArray']
    thisMean=numpy.mean(inputArray)
    thisSTD=numpy.std(inputArray)
    print "For ",npzfile," mean =",thisMean," +/- ", thisSTD
    
# form list of npz files
# for each file
#    compute the average for all pixels for all images
#    compute the STD for all pixels for all images
#    print out the results 




