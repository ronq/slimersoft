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
import pandas
import hdf5_cut_lib
import ROOT
import plot_pandas_lib

inputFile = sys.argv[1]
outputRootName=sys.argv[2] 

# define cut table 
cutTable="""
0.0     DBScan_Counts               9.e20       select
"""
#define variables for which we want 2D histograms 
pairsFor2D=[
["DBScan_Counts","DBScan_PeakHeight"],
["DBScan_Counts","DBScan_NumPixels"],
["DBScan_NumPixels","DBScan_PeakHeight"],
["DBScan_AvgPixelCount","DBScan_NumPixels"],
["DBScan_AvgPixelCount","DBScan_Counts"]
]
#open file and associated tables
#imageDataTable=pandas.read_hdf(inputFile,'ImageData')
inputStore=pandas.HDFStore(inputFile,mode='r')

# prepare output HDF5file
hdf5FileName=outputRootName +"_hdf5.h5"
outputStore=pandas.HDFStore(hdf5FileName,'w')

# prepare ROOT output 
outputROOTFileName=outputRootName + ".root"
newfile=ROOT.TFile(outputROOTFileName,'RECREATE') # open output right away to enable easy histogram output. 

# generate the cuts from the input cut table 
imageCuts=hdf5_cut_lib.hdf5_cut_lib(cutTable)

for key in inputStore.keys():                                   # cycle through each key in the file. Each key points to a DataFrame, so we're iterating through DataFrames
        inputTable=inputStore.get(key)                          # retrieve the DataFrame
        newTable = imageCuts.ApplyCuts(inputTable)              # apply cuts, if any, to this DataFrame   
        if newTable.shape[0] > 0:                               # only output if there are events in this DataFrame
            outputStore.append(key,newTable)                    # append the crunched DataFrame to the output file     
            plot_pandas_lib.plot_pandas(newTable,pairsFor2D)    # note that there's no need to pass the newfile object: PyRoot already has access to the file for writing
        
# the above works when the DataFrames are kept seperate. If we wish to correleate then things become more complicated.
# first enable links betweem the DataFrames by setting up dictionaries to enable fast lookups.
# psuedo code for this
# for index in General DataFrame # the index is the filepath
# for each other DataFrame:  
#   search for a match to teh filePath
#        if match found add the matching index to an array
#   add dictionary entry: key is filePath and value are matching indexes
# 
# then can cycle through the General DataFrame and fetch relevent information
# likely want to apply more cuts 
# likely want the ability plot variables between dataFrames, this will premet correlations to be studied 
#
# need to decide if this should be a seperate file, or be run in this one. 


newfile.Write()  # write all histograms to disk, redundant?
newfile.Close()
inputStore.close()
outputStore.close()

















