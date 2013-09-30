#! /usr/bin/env python
#
"""  This script combines data included in multiple HDF5 files and output 
     
     usage hdf5_sum.py  <path to input files> <output file name>
     
"""
import sys
import glob
import pandas
import tables

inputPath=sys.argv[1]
outputName=sys.argv[2]

# form file list for processing
inputList=glob.glob(inputPath)
# open output file 
newStore=pandas.HDFStore(outputName,mode='w')
#open each file and append contents to the new store
print "Processing ",len(inputList), " files"
numOpened=0
# first append all data into the new store
for newfile in inputList:
    try: 
        oldStore=pandas.HDFStore(newfile,mode='r')
        numOpened+=1
        for key in oldStore.keys():   # iterate over all tables in the file
            newStore.append(key,oldStore[key])     # and append them to be new file
        oldStore.close()  
    except tables.exceptions.HDF5ExtError:
        print "HDF5Ext Error in file", newfile   
        
# now reset the indices for the DataFrames, as the appending process will scramble them
for key in newStore.keys():
     (newStore[key]).reset_index(drop=True,inplace=True)  # modify the existing object, and do NOT add the old indices as a new column

newStore.close()
print "Successfully Processed", numOpened, "files"


