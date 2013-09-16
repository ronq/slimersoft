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
import cluster_output
import pandas
import shawfit_analysis
import shawcluster_analysis

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
            #self.imageArray=numpy.zeros( (self.imageSize,self.imageSize,number),dtype=numpy.uint16)
            self.imageArray=numpy.zeros( (self.imageSize,self.imageSize,number),dtype=numpy.float)
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
            #print self.backgroundAverageArray.dtype,self.imageArray.dtype
            self.imageArray[:,:,image_number]-=self.backgroundAverageArray  # do the subtraction in place
            self.imageArray[:,:,image_number]*=aboveBackground              # apply the mask, as unsigned 16 bit integers will cause pixels below background to "turn over" 
            # may want to zero out negative entries 
            #print self.imageArray[:,:,image_number]
            return
      #-------------------------------------------------------------------------------
      def ApplyThreshold(self,image_number):
            passThreshold=self.imageArray[:,:,image_number] > (self.thresholdInSigma*numpy.sqrt(self.backgroundVarArray))
            self.imageArray[:,:,image_number] *= passThreshold # this will modify the array to zero out anything below threshold 
      #-------------------------------------------------------------------------------      
      def ComputeGeneralVariables(self,image_number):
            self.imageAverage.append(numpy.mean(self.imageArray[:,:,image_number])) # compute image average
            self.imageVar.append(numpy.var(self.imageArray[:,:,image_number]))      # compute image variance  
            self.imageMax.append(numpy.amax(self.imageArray[:,:,image_number]))     # compute hottest pixel
            self.imageSum.append(self.imageArray[:,:,image_number].sum())           # compute sum of entire image  
            # compute the number of pixels 1,2,3,4,5 sigma above background
            # keep in mind that the image has already been subtracted, so only need to compare to the standard deviation
            relativeResidualArray=self.imageArray[:,:,image_number]/numpy.sqrt(self.backgroundVarArray) # converts the image to units of standard deviations
            self.hotPixels_1Sigma.append((relativeResidualArray > 1.0).sum())
            self.hotPixels_2Sigma.append((relativeResidualArray > 2.0).sum())
            self.hotPixels_3Sigma.append((relativeResidualArray > 3.0).sum())
            self.hotPixels_4Sigma.append((relativeResidualArray > 4.0).sum())
            self.hotPixels_5Sigma.append((relativeResidualArray > 5.0).sum())
            
            return
      
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
            #minPts=500.
            #eps = 5.0 # must be a float!!!!!
            minPts=700.
            eps=2.0
            
            dbscan.DoIt(self.imageArray[:,:,imageNumber],minPts,eps)
            return dbscan
      #-------------------------------------------------------------------------------
      def DoShawFit(self,imageNumber):
            shawfit=shawfit_analysis.shawfit_analysis()
            shawfit.DoIt(self.imageArray[:,:,imageNumber])
            
            return shawfit
      #------------------------------------------------------------------------------
      def DoShawCluster(self,imageNumber):
            shawcluster=shawcluster_analysis.shawcluster_analysis()
            shawcluster.DoIt(self.imageArray[:,:,imageNumber])
            
            return shawcluster
      #------------------------------------------------------------------------------
      
      def GetPeakInfo(self,imageNumber):
            return    
      #-------------------------------------------------------------------------------
      def PrepareResults(self):
            # general image parameters 
            self.output_fullFilePath=[]
            self.imageMax=[]
            self.imageAverage=[]
            self.imageVar=[]
            self.imageSum=[]
            self.hotPixels_1Sigma=[]
            self.hotPixels_2Sigma=[]
            self.hotPixels_3Sigma=[]
            self.hotPixels_4Sigma=[]
            self.hotPixels_5Sigma=[]
            self.generalDict={}
             
            return
      #-------------------------------------------------------------------------------
      def StoreGeneralResults(self,imageNumber):
            """ Will want to append some arrays here..."""
           
            # form dictionary of general results 
            generalDict={
                                 'ImagePath': [self.inputFileList[imageNumber]],
                                 'ImageMax' : self.imageMax,
                                 'ImageMean': self.imageAverage,
                                 'ImageVariance':  self.imageVar         ,
                                 'ImageSum':      self.imageSum          ,
                                 'HotPixels1Sigma':       self.hotPixels_1Sigma  ,
                                 'HotPixels2Sigma':       self.hotPixels_2Sigma  ,
                                 'HotPixels3Sigma':       self.hotPixels_3Sigma  ,
                                 'HotPixels4Sigma':       self.hotPixels_4Sigma  ,
                                 'HotPixels5Sigma':       self.hotPixels_5Sigma  
            }
            return generalDict
      #---------------------------------------------------------------------------
      def OpenHDF5File(self,root_name):
            hdf5FileName=root_name +"_hdf5.h5"
            store=pandas.HDFStore(hdf5FileName,'w')       
            return store
      #----------------------------------------------------------------------------------
      def CloseHDF5File(self,fileObject):
            fileObject.close()  
            return      
      #-------------------------------------------------------------------------------
      def OutputHDF5Results(self,store,general_results,kmeans_results,dbscan_results,shawfit_results,shawcluster_results):
            """ output into a PANDAS HDF5
            """
        
            # build PANDAS DataFrames and write to store the general results
            nameIndex=general_results['ImagePath']
            generalDF=pandas.DataFrame(general_results,index=nameIndex)  # include imagePath as the index, for fast lookups                       
            store.append('General_ImageData',generalDF) # this will make a table, which can be appended to
            
            # do the same for the DBSCAN results 
            if dbscan_results.foundClusters:
                dbscanDF=pandas.DataFrame(dbscan_results.dbscanDict)
                dbscanDF['ImagePath']= nameIndex*len(dbscanDF)  # add the imagePath to enable connection with other DataFrames 
                store.append('DBSCAN_ImageData',dbscanDF)
            # do the same for the kMeans results
            if kmeans_results.foundClusters:
                kmeansDF=pandas.DataFrame(kmeans_results.kmeansDict)
                kmeansDF['ImagePath']=nameIndex*len(kmeansDF)
                store.append('kMeans_ImageData',kmeansDF)                 
            if shawcluster_results.foundClusters:
                shawclusterDF=pandas.DataFrame(shawcluster_results.shawclusterDict)
                shawclusterDF['ImagePath']=nameIndex*len(shawclusterDF)
                store.append('ShawCluster_ImageData',shawclusterDF)                                      
            return
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
#bigA.PrepareResults()
bigA.LoadImages(numImages)
bigA.LoadBackground(backgroundNPZ)
hdf5File=bigA.OpenHDF5File(outputRootName)
for imageNumber in range(numImages):
    bigA.PrepareResults()
    bigA.SubtractBackground(imageNumber)
    bigA.ApplyThreshold(imageNumber)
    bigA.ComputeGeneralVariables(imageNumber)
    bigA.ApplyFilters(imageNumber)
    bigA.FindPeaks(imageNumber)
    bigA.GetPeakInfo(imageNumber)
    #bigA.StoreResults(imageNumber)
    # for debugging
    hotPixels=numpy.sum(bigA.imageArray[:,:,imageNumber] > 0)
    #print "Non-zero Pixel count and Sum:",hotPixels,imageSum
    kmeans_results=bigA.DoKmeans(imageNumber)
    dbscan_results=bigA.DoDBSCAN(imageNumber)
    #shawfit_results=bigA.DoShawFit(imageNumber)
    shawcluster_results=bigA.DoShawCluster(imageNumber)
    #kmeans_results.clusterfrac
    #if (hotPixels >= 500) or (imageSum > 60000):
    if (kmeans_results.clusterFrac < 0.4) or (kmeans_results.clusterFrac > 0.6):
        # 15 hot pixels --> 1.0 sigma
        # 300 hot pixels --> 0.5 sigma
        # 100 hot pixels --> 0.75 sigma?
        #print "Non-zero Pixel count and Sum:",hotPixels,bigA.imageArray[:,:,imageNumber].sum()
        #matplotlib.pyplot.imshow(bigA.imageArray[:,:,imageNumber] > 0, cmap=matplotlib.pyplot.cm.gray)  # for debugging
        #matplotlib.pyplot.show()
        #raw_input("Press a key to continue")
        #bigA.DoKmeans(imageNumber)
        pass
    general_results=bigA.StoreGeneralResults(imageNumber) 
    shawfit_results=[]
    bigA.OutputHDF5Results(hdf5File,general_results,kmeans_results,dbscan_results,shawfit_results,shawcluster_results)  
    
bigA.CloseHDF5File(hdf5File)
#print "Writing out Averaged Arrays"
#bigA.WriteAverageArrays(averageArrayFileName)            
            
            
