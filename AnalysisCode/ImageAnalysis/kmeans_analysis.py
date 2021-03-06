#! /usr/bin/env python
#
import numpy
import scipy
import scipy.cluster
import scipy.cluster.vq
import cluster_output
class kmeans_analysis:
      """ this class executes a k-means clustering analysis to a greyscale uint16 array

      """
      #------------------------------------------------------------------------------------------------------------------------------------------
      def __init__(self):
	  self.kmeansIterations=20
	  self.kmeansThreshold=1e-05
	  return
      
      #---------------------------------------------------------------------------- 
      def ComputeCenterOfEnergy(self):
            return
      #----------------------------------------------------------------------------
      def GenerateKmeansData(self):
            """ this will generate an array of 2D points, taking into account the value of the pixels
            """
            self.foundClusters=True # this algorithm will always find something
            kmeansDataList=[]
            totalCounts=float(self.imageArray.sum())
            runningTotal_ForX=0.0
            runningTotal_ForY=0.0
            #centerOfEnergyList=[]
            arrayIterator=numpy.nditer(self.imageArray,flags=['multi_index'])
            while not arrayIterator.finished:
                    position=arrayIterator.multi_index
                    weight=arrayIterator[0]
                    for i in range(weight): # assume integer
                        runningTotal_ForX+=float(position[0])
                        runningTotal_ForY+=float(position[1])
                        kmeansDataList.append(position)   # if a pixel weight is N, then add N entries to the list 
                    arrayIterator.iternext()       
            #self.centerOfEnergy=numpy.array( [ [(runningTotal_ForX/totalCounts)], [(runningTotal_ForY/totalCounts) ] ] )
            #centerofEnergyList.append([(runningTotal_ForX/totalCounts),(runningTotal_ForY/totalCounts)
            self.centerOfEnergy=numpy.array([[(runningTotal_ForX/totalCounts),(runningTotal_ForY/totalCounts)]])
            self.kmeansFeatures=numpy.array(kmeansDataList)
            return
      #---------------------------------------------------------------------------
      def WhitenFeatures(self):
            self.whitenedFeatures=scipy.cluster.vq.whiten(self.kmeansFeatures)
            return
      #---------------------------------------------------------------------------  
      def DoKmeans(self):
            #print "KMeans info:", numpy.shape(self.whitenedFeatures), numpy.shape(self.centerOfEnergy), self.centerOfEnergy
            
            #centers, distortion = scipy.cluster.vq.kmeans(self.whitenedFeatures,self.centerOfEnergy)
            ##centers, distortion = scipy.cluster.vq.kmeans(self.whitenedFeatures,k_or_guess=1)
            #code, distance = scipy.cluster.vq.vq(self.whitenedFeatures,centers)
            self.centers, self.distortion = scipy.cluster.vq.kmeans(self.kmeansFeatures,k_or_guess=2)
            self.code, self.distance = scipy.cluster.vq.vq(self.kmeansFeatures,self.centers)
            # debug code
            #print centers, distortion
            #print numpy.shape(code), numpy.sum(code)
            return
      #---------------------------------------------------------------------------
      def AnalyzeResults(self):
            # get the number of points (actually counts) in the total data
            # get the number of points (actually counts) in the cluster
            # look at the distortion too
            totalpoints=self.kmeansFeatures.size/2. # each point is 2x1
            self.clusterpoints=[self.code.sum()]  # note that this is the integral energy of the cluster 
            self.clusterFrac=[element/totalpoints for element in self.clusterpoints]
            return
      
      #---------------------------------------------------------------------------
      def GenerateOutput(self):
            """ load relevant results into standard output variables
            """
            # want all outputs to have the same dimensional length, so form some dummy parameters
            dummyArray=[-999.0 for element in self.clusterpoints] 
            numClustersArray=[len(self.clusterpoints) for element in self.clusterpoints] 
            self.kmeansDict={
            'kmeans_NumPixels':dummyArray,
            'kmeans_Counts':self.clusterpoints,
            'kmeans_ClusterFrac': self.clusterFrac,
            'kmeans_AvgPixelCount':dummyArray,
            'kmeans_PositionX': dummyArray,
            'kmeans_PositionXVariance': dummyArray, 
            'kmeans_PositionY':dummyArray,
            'kmeans_PositionYVariance':dummyArray,
            'kmeans_PeakHeight': dummyArray,
            'kmeans_NumClusters': numClustersArray
            }
            return
      #---------------------------------------------------------------------------
      def DoIt(self,inputArray):
            #self.clusterOutput=cluster_output.cluster_output()
            self.imageArray=inputArray
            #print "generating KMeans Data"
            self.GenerateKmeansData() # prepare the data first
            # get estimate of "center of energy"
            #print "Whitening Features"
            self.WhitenFeatures() # whiten
            #print "Running Kmeans"
            self.DoKmeans()# run the kmeans test
            # check for a second cluster
            self.AnalyzeResults() # get cluster info
            self.GenerateOutput() 
            #print "Kmeans",self.clusterpoints,self.clusterFrac,self.distortion
            return    
      #------------------------------------------------------------------------------         
      
      
                
