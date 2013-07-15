#! /usr/bin/env python
#
import scipy
import scipy.cluster
import scipy.cluster.vq
class kmeans_analysis(self):
      """ this class executes a k-means clustering analysis to a greyscale uint16 array

      """
      #------------------------------------------------------------------------------------------------------------------------------------------
      def __init__(self,self.imageArray):
      
	  self.kmeansIterations=20
	  self.kmeansThreshold=1e-05
	  return
      #---------------------------------------------------------------------------
      def DoIt(self):
            # get estimate of "center of mass"
            # prepare the data first
            # get estimate of "center of energy"
            # whiten
            # run the kmeans test
            # check for a second cluster
            # get cluster info
            return
      #---------------------------------------------------------------------------- 
      def ComputeCenterOfEnergy(self,self.imageArray)
            return
      #----------------------------------------------------------------------------
      def GenerateKmeansData(self,self.imageArray):
            """ this will generate an array of 2D points, taking into account the value of the pixels
            """
            kmeansDataList=[]
            totalCounts=float(self.imageArray.sum())
            runningTotal_ForX=0.0
            runningTotal_ForY=0.0
            arrayIterator=numpy.nditer(self.imageArray,flags=['multi_index'])
                while not arrayIterator.finished:
                    position=arrayIterator.multi_index
                    weight=arrayIterator[0]
                    for i in weight: # assume integer
                        runningTotal_ForX+=float(position[0])
                        runningTotal_ForY+=float(position[1])
                        kmeansDataList.append(position)   # if a pixel weight is N, then add N entries to the list 
                    arrayIterator.iternext()       
            self.centerOfEnergy=numpy.array(  (runningTotal_ForX/totalCounts), (runningTotal_ForY/totalCounts) 
            self.kmeansFeatures=numpy.array(kmeansDataList)
            return
      #---------------------------------------------------------------------------
      def WhitenFeatures(self):
            self.whitenedFeatures=scipy.cluster.vq.whiten(self.kmeansFeatures)
            return
      #---------------------------------------------------------------------------  
      def DoKmeans(self):
            centers, distortion = scipy.cluster.vq.kmeans(self.whitenedFeatures,self.centerOfEnergy)
            code, distance = scipy.cluster.vq.vq(self.whitenedFeatures,centers)
            # debug code
            print code
            
      
      
                
