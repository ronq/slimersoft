#! /usr/bin/env python
#
"""  This script will generate a file containing two numpy arrays: one is a array representing the average of all pixel counts, the other is an array representing the variance of all pixel counts.

     Extra text
     
     usage:  background_average.py  [path to images to average] [base file name for output] 
     
     
     
"""
import sys

import math
import numpy
import scipy
import Image


class average_image:
      "Class for averaging images"
      
      #------------------------------------------------------------------------------------------------------------------------------------------
      def __init__(self):
      
	  self.inputWildCard=""
	  self.inputFileList=[]
	  self.imageSize=512
	  return
      #------------------------------------------------------------------------------------------------------------------------------------------
      def MakeInputList(self,inputList):
            """ form input file list """
            import glob
            self.inputWildCard=inputList
            fileList=glob.glob(self.inputWildCard)
            self.inputFileList=fileList
            return len(fileList)
      #------------------------------------------------------------------------------------------------------------------------------------------
      def Load1Image(self,inputFile):
            """ load one image into memory, using PIL then translating to a numpy array"""
            pil_im=Image.open(inputFile)
            inputData=numpy.array(pil_im.getdata()).reshape(pil_im.size[0], pil_im.size[1])
            return inputData 
      #------------------------------------------------------------------------------------------------------------------------------------------      
      def LoadImages(self,number):
            """ load <number> images into the overall array, and also calculate per image statistics"""
            # create the arrays first
            #print "Creating Array"
            self.averageArray=numpy.zeros( (self.imageSize,self.imageSize))
            self.VarArray=numpy.zeros( (self.imageSize,self.imageSize))
            # use Knuth and Welford's running variance calculation, may need to use better than float for this
            n=0
            M2Array=numpy.zeros( (self.imageSize,self.imageSize))
            for i in range(number):
                n+=1
                inputData=self.Load1Image(self.inputFileList[i]) 
                delta = inputData - self.averageArray
                self.averageArray+=delta/n
                M2Array += delta*(inputData - self.averageArray)
            self.VarArray = M2Array/(n-1)
            print self.averageArray, self.VarArray
            return      
      #------------------------------------------------------------------------------------------------------------------------------------------
      def ComputeAverage(self):
            self.averageArray=numpy.mean(self.imageArray,axis=2)
      #------------------------------------------------------------------------------------------------------------------------------------------
      def ComputeVar(self):
            #self.STDArray=numpy.std(self.imageArray,axis=2)   # hangs on large data  
            self.VarArray=numpy.var(self.imageArray,axis=2)    
      #----------------------------------------------------------------------------
      def WriteAverageArrays(self,outputName):
            numpy.savez(outputName,averageArray=self.averageArray,VarArray=self.VarArray) 
            return                              
      #---------------------------------------------------------------------------  
      def DoIt(self):
            return
##############################################################################	  
# extra methods

#############################################################################



# get arguments
inputList=sys.argv[1]
outputRootName=sys.argv[2]

averageArrayFileName=outputRootName+"_average_array.npz"

# initialize class
bigA=average_image()
numImages=bigA.MakeInputList(inputList)
print "Number of Images:",numImages
bigA.LoadImages(numImages)
print "Computing Overall Average"
#bigA.ComputeAverage()
print "Computing Overall Variance"
#bigA.ComputeVar()
print "Writing out Averaged Arrays"
bigA.WriteAverageArrays(averageArrayFileName)





