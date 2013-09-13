#! /usr/bin/env python
#
"""  This script combines data included in multiple HDF5 files and output 
     
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
newStore=pandas.HDFStore(outputName,mode='w')
#open each file and append contents to the new store
print "Processing ",len(inputList), " files"
for newfile in inputList:
    imageDataTable=pandas.read_hdf(newfile,'ImageData')
    oldStore=pandas.HDFStore(newfile,mode='r')
    for key in oldStore.keys():   # iterate over all tables in the file
        newStore.append(key,oldStore[key])     # and append them to be new file
    oldStore.close()    
newStore.close()


