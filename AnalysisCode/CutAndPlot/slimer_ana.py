#! /usr/bin/env python
#
"""  This script will parse an hdf5 file, apply cuts, and make some histograms (maybe an smaller hdf5 file too) 

     I'll want to include the ability to include the cuts table as a comment in the output hdf5 file
     
     usage:  image_analyis.py  [path to images to input hdf5 file]  [root name for output]
     
     
     
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
import hdf5_cut_lib
import ROOT
import plot_pandas_lib

inputFile = sys.argv[1]
outputRootName=sys.argv[2] 

# define cut table 
cutTable="""
0.0     DBScan_Counts               9.e20       select
1.0     DBScan_NumClusters          4.0         select
"""
#define variables for which we want 2D histograms 
pairsFor2D=[
["DBScan_Counts","DBScan_PeakHeight"],
["DBScan_Counts","DBScan_NumPixels"],
["DBScan_NumPixels","DBScan_PeakHeight"],
]




#open file
imageDataTable=pandas.read_hdf(inputFile,'ImageData')

# apply cuts 
new_imageDataTable=(hdf5_cut_lib.hdf5_cut_lib(imageDataTable,cutTable)).result


# output the crunched DataFrame to a new hdf5 file
hdf5FileName=outputRootName +"_hdf5.h5"
store=pandas.HDFStore(hdf5FileName)
store.append('ImageData',new_imageDataTable) # this will make a table, which can be appended to
store.close()

# now book and fill histograms 
outputROOTFileName=outputRootName + ".root"
newfile=ROOT.TFile(outputROOTFileName,'RECREATE') # open output right away to enable easy histogram output

pairs=["var1","var2"]
plot_pandas_lib.plot_pandas(new_imageDataTable,pairsFor2D)




newfile.Write()  # write all histograms to disk
newfile.Close()



















