#! /usr/bin/env python
#
"""  This script combine data included in multiple HDF5 files and output 
     
     usage hdf5_sum.py  <path to input files> <output file name>
     
"""
import sys
import glob
import pandas


inputPath=sys.argv[1]
outputName=sys.argv[2]

# form file list for processing
inputList=glob.glob(inputPath)
# open output file 
store=pandas.HDFStore(outputName,mode='w')
#open each file and append contents to the new store
print "Processing ",len(inputList), " files"
for newfile in inputList:
    imageDataTable=pandas.read_hdf(newfile,'ImageData')
    store.append('ImageData',imageDataTable)
store.close()

