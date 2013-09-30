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
newStore=pandas.HDFStore(outputName,mode='w')
#open each file and append contents to the new store
print "Processing ",len(inputList), " files"
for newfile in inputList:
    #imageDataTable=pandas.read_hdf(newfile,'ImageData')
    oldStore=pandas.HDFStore(newfile,mode='r')
    print oldStore.items()
    for key in oldStore.keys():
        newStore.append(key,oldStore[key])
    oldStore.close()    
    #for path,tables in oldStore.items():
    #     print tables
    #     newStore.append(path,tables)
    # want to get a list of tables in a store
    
    #store.keys
    #store.items
    #newStore.append('ImageData',imageDataTable)
    
newStore.close()


