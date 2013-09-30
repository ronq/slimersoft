#! /usr/bin/env python
#
"""  This script will test some features of PANDAS DataFrames 

     Extra text
     
     usage:  datafrane_tests.py
     
     
     
"""
import sys

import math
import numpy
import scipy
import Image

import pandas


#hdf5FileName="dataframe_tests_hdf5.h5"
#store=pandas.HDFStore(hdf5FileName,'w')  

# define some long arrays 
array1=numpy.arange(50000000.,dtype=numpy.int64)
array2=numpy.arange(50000000.,dtype=numpy.int64)
array3=numpy.arange(50000000.,dtype=numpy.int64)
array4=numpy.arange(50000000.,dtype=numpy.int64)
array2*=2.
array3*=10.
array4*=100.

indexedDict={'Array2':array2,'Array3':array3,'Array4':array4}
nonindexedDict={'Array1':array1,'Array2':array2,'Array3':array3,'Array4':array4}

indexedFrame=pandas.DataFrame(indexedDict,index=array1)
nonindexedFrame=pandas.DataFrame(nonindexedDict)

# now slice and dice
print indexedFrame.head()

print "----------------------"
print nonindexedFrame.head()

print len(indexedFrame)

nonindexedFrame['new_col']= range(1,len(nonindexedFrame)+1)
print nonindexedFrame.head()


print "=============="
#for i in range(1000):
     #object1=indexedFrame.loc[i]
     #object2=nonindexedFrame[nonindexedFrame['Array1'] == i]

#store.append('ImageData',df) # this will make a table, which can be appended to
#store.close()
