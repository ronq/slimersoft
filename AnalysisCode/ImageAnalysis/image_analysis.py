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
            self.imageAverage=numpy.mean(self.imageArray[:,:,image_number]) # compute image average
            self.imageVar=numpy.var(self.imageArray[:,:,image_number])      # compute image variance  
            self.imageMax=numpy.amax(self.imageArray[:,:,image_number])     # compute hottest pixel
            self.imageSum=self.imageArray[:,:,image_number].sum()           # compute sum of entire image  
            # compute the number of pixels 1,2,3,4,5 sigma above background
            # keep in mind that the image has already been subtracted, so only need to compare to the standard deviation
            relativeResidualArray=self.imageArray[:,:,image_number]/numpy.sqrt(self.backgroundVarArray) # converts the image to units of standard deviations
            self.hotPixels_1Sigma=(relativeResidualArray > 1.0).sum()
            self.hotPixels_2Sigma=(relativeResidualArray > 2.0).sum()
            self.hotPixels_3Sigma=(relativeResidualArray > 3.0).sum()
            self.hotPixels_4Sigma=(relativeResidualArray > 4.0).sum()
            #self.hotPixels_5Sigma=(relativeResidualArray > 5.0).sum()
            self.hotPixels_5Sigma=(relativeResidualArray > 20.0).sum()
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
            
            return 
      #------------------------------------------------------------------------------
      def DoShawCluster(self,imageNumber):
            shawcluster=shawcluster_analysis.shawcluster_analysis()
            shawcluster.DoIt(self.imageArray[:,:,imageNumber])
            
            return 
      #------------------------------------------------------------------------------
      
      def GetPeakInfo(self,imageNumber):
            return    
      #-------------------------------------------------------------------------------
      def PrepareResults(self):
            # general image parameters 
            self.output_fullFilePath=[]
            self.output_imageMax=[]
            self.output_imageMean=[]
            self.output_imageVariance=[]
            self.output_imageSum=[]
            self.output_hotpixels1Sigma=[]
            self.output_hotpixels2Sigma=[]
            self.output_hotpixels3Sigma=[]
            self.output_hotpixels4Sigma=[]
            self.output_hotpixels5Sigma=[]
            # output of dbscan analysis. This is an array of objects. 
            self.output_dbscan_results=[]
            self.output_kmeans_results=[]
            return
      #-------------------------------------------------------------------------------
      def StoreResults(self,imageNumber,dbscan_results,kmeans_results):
            """ Will want to append some arrays here..."""
            #
            self.output_fullFilePath.append(self.inputFileList[imageNumber])
            # general image parameters
            self.output_imageMax.append(self.imageMax)
            self.output_imageMean.append(self.imageAverage)
            self.output_imageVariance.append(self.imageVar)
            self.output_imageSum.append(self.imageSum)
            self.output_hotpixels1Sigma.append(self.hotPixels_1Sigma)
            self.output_hotpixels2Sigma.append(self.hotPixels_1Sigma)
            self.output_hotpixels3Sigma.append(self.hotPixels_1Sigma)
            self.output_hotpixels4Sigma.append(self.hotPixels_1Sigma)
            self.output_hotpixels5Sigma.append(self.hotPixels_1Sigma)
            
            #dbscan parameters
            self.output_dbscan_results.append(dbscan_results)
            
            #kmeans parameters
            self.output_kmeans_results.append(kmeans_results)
            
            
            
            return
      #-------------------------------------------------------------------------------
      def OutputASCIIResults(self,root_name):
            """ write results in ASCII format, each line corresponding to an image. This way I can 'cat' everything together later on"""
            #
            #
            #  this is what I want to calculate for each method:
            #  position of cluster -- weighted mean or peak position
            #  "width" of cluster -- perhaps the standard deviation or variance of the cluster?
            #  area of the cluster --number of pixels above a threshold
            #  peak of the cluster -- highest pixel count inside
            #  integrated counts inside cluster
            #  background outside the cluster
            #
            #
            asciiFileName=root_name+"_ascii.dat"
            asciiFile=open(asciiFileName,'w')
            for i in range(len(self.output_fullFilePath)):
                outputString= (self.output_fullFilePath[i] + " " +
                              str(self.output_imageMax[i]) + " " +
                              str(self.output_imageMean[i]) + " " +
                              str(self.output_imageVariance[i]) + " " +
                              str(self.output_imageSum[i]) + " " +
                              str(self.output_hotpixels1Sigma[i]) + " " +
                              str(self.output_hotpixels2Sigma[i]) + " " +
                              str(self.output_hotpixels3Sigma[i]) + " " +
                              str(self.output_hotpixels4Sigma[i]) + " " +
                              str(self.output_hotpixels5Sigma[i]) + " " +
                              str(self.output_dbscan_results[i].clusterOutput.outputClusterSize)+ " " +
                              str(self.output_dbscan_results[i].clusterOutput.outputCounts)+ " " +
                              str(self.output_dbscan_results[i].clusterOutput.outputClusterFrac)+ " " +
                              str(self.output_dbscan_results[i].clusterOutput.outputAvgPixelCount)+ " " +
                              str(self.output_dbscan_results[i].clusterOutput.outputPosition)+ " " +
                              str(self.output_dbscan_results[i].clusterOutput.outputPositionVariance)+ " " +
                              str(self.output_dbscan_results[i].clusterOutput.outputPeakHeight)+ " " +
                              str(self.output_dbscan_results[i].clusterOutput.outputNumberOfClusters)+ " " +
                              str(self.output_kmeans_results[i].clusterOutput.outputClusterSize)+ " " +
                              str(self.output_kmeans_results[i].clusterOutput.outputCounts)+ " " +
                              str(self.output_kmeans_results[i].clusterOutput.outputClusterFrac)+ " " +
                              str(self.output_kmeans_results[i].clusterOutput.outputAvgPixelCount)+ " " +
                              str(self.output_kmeans_results[i].clusterOutput.outputPosition)+ " " +
                              str(self.output_kmeans_results[i].clusterOutput.outputPositionVariance)+ " " +
                              str(self.output_kmeans_results[i].clusterOutput.outputPeakHeight)+ " " +
                              str(self.output_kmeans_results[i].clusterOutput.outputNumberOfClusters)+ " " +
                              "\n")
                                
                asciiFile.write(outputString)
            asciiFile.close()     
            return
      #-------------------------------------------------------------------------------
      def OutputHDF5Results(self,root_name):
            """ output into a PANDAS HDF5
            """
            hdf5FileName=root_name +"_hdf5.h5"
            store=pandas.HDFStore(hdf5FileName,'w')
            df=pandas.DataFrame({'ImagePath': self.output_fullFilePath,
                                 'ImageMax' : self.output_imageMax,
                                 'ImageMean': self.output_imageMean,
                                 'ImageVariance':           self.output_imageVariance,
                                 'ImageSum':                self.output_imageSum,
                                 'HotPixels1Sigma':         self.output_hotpixels1Sigma,
                                 'HotPixels2Sigma':         self.output_hotpixels2Sigma,
                                 'HotPixels3Sigma':         self.output_hotpixels3Sigma,
                                 'HotPixels4Sigma':         self.output_hotpixels4Sigma,
                                 'HotPixels5Sigma':         self.output_hotpixels5Sigma,
                                 'DBScan_NumPixels':        [result.clusterOutput.outputClusterSize for result in self.output_dbscan_results],
                                 'DBScan_Counts':           [result.clusterOutput.outputCounts for result in self.output_dbscan_results],
                                 'DBScan_ClusterFrac':      [result.clusterOutput.outputClusterFrac for result in self.output_dbscan_results],
                                 'DBScan_AvgPixelCount':    [result.clusterOutput.outputAvgPixelCount for result in self.output_dbscan_results],
                                 'DBScan_PositionX':         [result.clusterOutput.outputPosition[0] for result in self.output_dbscan_results],
                                 'DBScan_PositionXVariance': [result.clusterOutput.outputPositionVariance[0] for result in self.output_dbscan_results],
                                 'DBScan_PositionY':         [result.clusterOutput.outputPosition[1] for result in self.output_dbscan_results],
                                 'DBScan_PositionYVariance': [result.clusterOutput.outputPositionVariance[1] for result in self.output_dbscan_results],
                                 'DBScan_PeakHeight':       [result.clusterOutput.outputPeakHeight for result in self.output_dbscan_results],
                                 'DBScan_NumClusters':      [result.clusterOutput.outputNumberOfClusters for result in self.output_dbscan_results],
                                 'kmeans_NumPixels':        [result.clusterOutput.outputClusterSize for result in self.output_kmeans_results],
                                 'kmeans_Counts':           [result.clusterOutput.outputCounts for result in self.output_kmeans_results],
                                 'kmeans_ClusterFrac':      [result.clusterOutput.outputClusterFrac for result in self.output_kmeans_results],
                                 'kmeans_AvgPixelCount':    [result.clusterOutput.outputAvgPixelCount for result in self.output_kmeans_results],
                                 'kmeans_PositionX':         [result.clusterOutput.outputPosition[0] for result in self.output_kmeans_results],
                                 'kmeans_PositionXVariance': [result.clusterOutput.outputPositionVariance[0] for result in self.output_kmeans_results],
                                 'kmeans_PositionY':         [result.clusterOutput.outputPosition[1] for result in self.output_kmeans_results],
                                 'kmeans_PositionYVariance': [result.clusterOutput.outputPositionVariance[1] for result in self.output_kmeans_results],
                                 'kmeans_PeakHeight':       [result.clusterOutput.outputPeakHeight for result in self.output_kmeans_results],
                                 'kmeans_NumClusters':      [result.clusterOutput.outputNumberOfClusters for result in self.output_kmeans_results]
                                 })                    
            store.append('ImageData',df) # this will make a table, which can be appended to
            store.close()
            
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
bigA.PrepareResults()
bigA.LoadImages(numImages)
bigA.LoadBackground(backgroundNPZ)
for imageNumber in range(numImages):
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
    shawfit_results=bigA.DoShawFit(imageNumber)
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
    bigA.StoreResults(imageNumber,dbscan_results,kmeans_results)       
bigA.OutputASCIIResults(outputRootName)  
bigA.OutputHDF5Results(outputRootName)  
#print "Writing out Averaged Arrays"
#bigA.WriteAverageArrays(averageArrayFileName)            
            
            
