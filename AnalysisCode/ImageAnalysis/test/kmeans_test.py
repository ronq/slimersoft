#! /usr/bin/env python
#
import numpy
import scipy
import scipy.cluster
import scipy.cluster.vq
import random

testList=[]
for i in range(1000):
    testList.append([random.randint(100.,110.),random.randint(100.,110.)])
for j in range(100):
    testList.append([random.randint(10000.,11000.),random.randint(10000.,11000.)])
#testList.append([10000.,10000.])     
#testArray=numpy.array([[100.,100.],[110.,100.],[100.,110.], [110.,110.], [10000.,10000.]])    
testArray=numpy.array(testList)  
#whitenedArray=scipy.cluster.vq.whiten(testArray)
whitenedArray=testArray
centers, distortion = scipy.cluster.vq.kmeans(whitenedArray,k_or_guess=10)
code, distance = scipy.cluster.vq.vq(whitenedArray,centers)
# debug code
print centers
print distortion
print code
print distance
