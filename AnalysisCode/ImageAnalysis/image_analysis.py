#! /usr/bin/env python
#
"""  This script will generate resulting observables on one or more images

     Extra text
     
     usage:  image_analyis.py  [path to images to analyze] [path to background npz file] [base file name for output] 
     
     
     
"""
import sys

import math
import numpy
import scipy
import Image
import matplotlib.pyplot
import kmeans_analysis
import dbscan_analysis

class analyze_images:
      "Class for analyzing images"
      
      #------------------------------------------------------------------------------------------------------------------------------------------
      def __init__(self):
      
	  self.inputWildCard=""
	  self.inputFileList=[]
	  self.imageSize=512
	  self.thresholdInSigma=0.75
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
            print "opening ", inputFile
            pil_im=Image.open(inputFile)
            inputData=numpy.array(pil_im.getdata()).reshape(pil_im.size[0], pil_im.size[1])
            return inputData 
      #------------------------------------------------------------------------------------------------------------------------------------------      
      def LoadImages(self,number):
            """ load <number> images into the overall array, and also calculate per image statistics"""
            # create the arrays first
            #print "Creating Array"
            self.imageArray=numpy.zeros( (self.imageSize,self.imageSize,number),dtype=numpy.uint16)
            for i in range(number):
                self.imageArray[:,:,i] = self.Load1Image(self.inputFileList[i]) 
            return    
      #------------------------------------------------------------------------------------------------------------------------------------------
      def LoadBackground(self,inputFile):
                backgroundAverageInfo=numpy.load(inputFile)
                #print backgroundAverageInfo.files
                self.backgroundAverageArray=backgroundAverageInfo['averageArray'] 
                try: 
                    self.backgroundVarArray=backgroundAverageInfo['VarArray'] 
                    #print "Got VarArray"
                except:
                    self.backgroundVarArray=backgroundAverageInfo['STDArray']
                    #print "Got STDArray"
                return    
      #------------------------------------------------------------------------------------------------------------------------------------------      
      def ComputeAverage(self):
            self.averageArray=numpy.mean(self.imageArray,axis=2)
            return
      #------------------------------------------------------------------------------------------------------------------------------------------
      def ComputeVar(self):
            #self.STDArray=numpy.std(self.imageArray,axis=2)   # hangs on large data  
            self.VarArray=numpy.var(self.imageArray,axis=2)    
            return
      #----------------------------------------------------------------------------
      def WriteAverageArrays(self,outputName):
            numpy.savez(outputName,averageArray=self.averageArray,VarArray=self.VarArray) 
            return                              
      #---------------------------------------------------------------------------  
      def SubtractBackground(self,image_number):
            aboveBackground=self.imageArray[:,:,image_number] > self.backgroundAverageArray  # get pixels above background, to serve as a mask
            self.imageArray[:,:,image_number]-=self.backgroundAverageArray  # do the subtraction in place
            self.imageArray[:,:,image_number]*=aboveBackground              # apply the mask, as unsigned 16 bit integers will cause pixels below background to "turn over" 
            # may want to zero out negative entries 
            #print self.imageArray[:,:,image_number]
            return
      #-------------------------------------------------------------------------------
      def ApplyThreshold(self,image_number):
            passThreshold=self.imageArray[:,:,image_number] > (self.thresholdInSigma*self.backgroundVarArray)
            self.imageArray[:,:,image_number] *= passThreshold # this will modify the array to zero out anything below threshold 
            
      #-------------------------------------------------------------------------------
      def ApplyFilters(self,image_number):
            """ Apply filters to an image array. I may want to make a new array to store this info, as I may want access to the original"""
            
            return
      #-------------------------------------------------------------------------------
      def FindPeaks(self,imageNumber):
            return
      #-------------------------------------------------------------------------------
      def DoKmeans(self,imageNumber):
            kmeans=kmeans_analysis.kmeans_analysis()
            kmeans.DoIt(self.imageArray[:,:,imageNumber])
            return kmeans
      #-------------------------------------------------------------------------------
      def DoDBSCAN(self,imageNumber):
            dbscan=dbscan_analysis.dbscan_analysis()
            dbscan.DoIt(self.imageArray[:,:,imageNumber])
            return dbscan
      #-------------------------------------------------------------------------------
      def GetPeakInfo(self,imageNumber):
            return    
      #-------------------------------------------------------------------------------
      def StoreResults(self,imageNumber):
            """ Will want to append some arrays here..."""
            return
      #-------------------------------------------------------------------------------
      def OutputResults(self):
            """ write results in ASCII format, each line corresponding to an image. This way I can 'cat' everything together later on"""
            return
      #-------------------------------------------------------------------------------
      #---------------------------------------------------------------------------
      def DoIt(self):
            return
            
            
#---------------------------------------------------------
# get arguments
inputList=sys.argv[1]
backgroundNPZ=sys.argv[2]
outputRootName=sys.argv[3]

# initialize class
bigA=analyze_images()
numImages=bigA.MakeInputList(inputList)
print "Number of Images:",numImages
bigA.LoadImages(numImages)
bigA.LoadBackground(backgroundNPZ)
for imageNumber in range(numImages):
    bigA.SubtractBackground(imageNumber)
    bigA.ApplyThreshold(imageNumber)
    bigA.ApplyFilters(imageNumber)
    bigA.FindPeaks(imageNumber)
    bigA.GetPeakInfo(imageNumber)
    bigA.StoreResults(imageNumber)
    # for debugging
    hotPixels=numpy.sum(bigA.imageArray[:,:,imageNumber] > 0)
    imageSum=bigA.imageArray[:,:,imageNumber].sum()
    print "Non-zero Pixel count and Sum:",hotPixels,imageSum
    kmeans_results=bigA.DoKmeans(imageNumber)
    dbresults_results=bigA.DoDBSCAN(imageNumber)
    #kmeans_results.clusterfrac
    #if (hotPixels >= 500) or (imageSum > 60000):
    if (kmeans_results.clusterFrac < 0.4) or (kmeans_results.clusterFrac > 0.6):
        # 15 hot pixels --> 1.0 sigma
        # 300 hot pixels --> 0.5 sigma
        # 100 hot pixels --> 0.75 sigma?
        #print "Non-zero Pixel count and Sum:",hotPixels,bigA.imageArray[:,:,imageNumber].sum()
        matplotlib.pyplot.imshow(bigA.imageArray[:,:,imageNumber] > 0, cmap=matplotlib.pyplot.cm.gray)  # for debugging
        matplotlib.pyplot.show()
        raw_input("Press a key to continue")
        #bigA.DoKmeans(imageNumber)
        
        
bigA.OutputResults()    
#print "Writing out Averaged Arrays"
#bigA.WriteAverageArrays(averageArrayFileName)            
            
            