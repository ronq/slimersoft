#! /usr/bin/env python
#
"""  This script will parse an hdf5 file, apply cuts, and make some histograms (maybe an smaller hdf5 file too) 

     Extra text
     
     usage:  image_analyis.py  [path to images to input hdf5 file]  [
     
     
     
"""
import sys

import math
import numpy
import scipy
#import Image
#import matplotlib.pyplot
#import kmeans_analysis
#import dbscan_analysis
#import cluster_output
import pandas


inputFile = sys.argv[1]
outputRootName=sys.argv[2] 


cutTable="""
0.0     DBScan_Counts               9.e20       select
1.0     DBScan_NumClusters          4.0         select
"""





#open file
imageDataTable=pandas.read_hdf(inputFile,'ImageData')

#print imageDataTable

# now form a bunch of boolean masks to apply to the data later
energyCut=imageDataTable['DBScan_Counts'] > 0.0
numClusterCut=(imageDataTable['DBScan_NumClusters'] > 1) & (imageDataTable['DBScan_NumClusters'] < 4)






# apply cuts 
new_imageDataTable=imageDataTable[energyCut & numClusterCut]
print new_imageDataTable
