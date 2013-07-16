#! /usr/bin/env python
#
"""  This script will test numpy iterators

     
"""
import sys

import math
import numpy


# create a matrix using a range
arrayLength=100
testArray0=numpy.arange(0,arrayLength)
testArray1=numpy.arange(arrayLength,arrayLength*2)
testArray2=numpy.arange(arrayLength*2,arrayLength*3)
testArray=numpy.array([testArray0,testArray1,testArray2])

print testArray
# setup the iterator
arrayIterator=numpy.nditer(testArray,flags=['multi_index'])
while not arrayIterator.finished:
                    position=arrayIterator.multi_index
                    counts=arrayIterator[0]
                    print position,counts , arrayIterator[0], arrayIterator[0]
                    print "Direct access : ",testArray[position]
                    arrayIterator2=numpy.nditer(testArray.copy(),flags=['multi_index'])
                    while not arrayIterator2.finished:
                        positionPrime=arrayIterator.multi_index
                        countsPrime=arrayIterator[0]
                        print arrayIterator[0], arrayIterator2[0]
                        arrayIterator2.iternext()  
                    arrayIterator.iternext()  

# start looping
# see if mutliple referrals to the iterator results in incrementing
# see if I can get matrix elements by reference during iteration


