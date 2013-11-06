#! /usr/bin/env python
#
import numpy
import sklearn
import sklearn.cluster
#import scipy
#import scipy.cluster
#import scipy.cluster.vq
import math
import cluster_output

import cluster_position


class dbscan_implementation:
    """  this is a fairly generic implemenation of the DBSCAN algorithm, except it is tailored for use on sqaure images
    
    
         it was adapted from this pseudocode:
   DBSCAN(D, eps, MinPts)
   C = 0
   for each unvisited point P in dataset D
      mark P as visited
      NeighborPts = regionQuery(P, eps)
      if sizeof(NeighborPts) < MinPts
         mark P as NOISE
      else
         C = next cluster
         expandCluster(P, NeighborPts, C, eps, MinPts)
          
expandCluster(P, NeighborPts, C, eps, MinPts)
   add P to cluster C
   for each point P' in NeighborPts 
      if P' is not visited
         mark P' as visited
         NeighborPts' = regionQuery(P', eps)
         if sizeof(NeighborPts') >= MinPts
            NeighborPts = NeighborPts joined with NeighborPts'
      if P' is not yet member of any cluster
         add P' to cluster C
          
regionQuery(P, eps)
   return all points within P's eps-neighborhood (including P)
    
    
    """

#------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self,input_image,input_minpts,input_eps):
        # input data and DBSCAN parameters 
        self.imageArray=input_image
        self.MinPts=input_minpts
        self.eps=input_eps  # must be a float!
        #self.imageArray=imput_image
        # extract the image size, assume it is square
        self.imageSize=input_image.shape[0] 
        
        # now initialize the pixelID array. This is the final product of the dbscan algorithm.
        #                                   It marks each point in an image with a particular ID, either zero (-2) noise (-1) or a cluster (positive integer)  
        self.pixelID=numpy.zeros((512,512)) 
        # intialize the overlap array: this indicates if pixels may be shared between clusters, which should only be the case with edge points 
        self.pixelOverlaps=numpy.zeros((512,512)) 
        # initialize working arrays 
        self.pixelVisited=numpy.zeros((512,512))   # this will mark the pixels as visited 
        self.tempPixels=numpy.zeros((self.imageSize,self.imageSize)) # for internal use only----provides a quick way of generating a zero matrix
        self.dbscan()   # run the algorithm
        return
#-----------------------------------------------------------------------------------------------------------   
    def dbscan(self):
        C=0 # this marks the cluster number
        arrayIterator=numpy.nditer(self.imageArray,flags=['multi_index'])
        while not arrayIterator.finished:
              position=arrayIterator.multi_index
              counts=arrayIterator[0]
              if not self.pixelVisited[position]:     
                    self.pixelVisited[position]=True
                    if counts: # don't try to find a cluster when the pixel is zero <<this is my own logic!>>
                        neighborPixels,neighborPixelsSum  = self.regionQuery(position) # neighborPixels will be a copy of the imageArray, with all but the neighbor pixels masked
                        #print neighborPixels.sum(),neighborPixelsSum
                        if neighborPixelsSum < self.MinPts:
                            if self.pixelID[position] > 0:
                                print "About to Mark clustered point as noise!"
                            self.pixelID[position] = -1  # mark this position as noise
                        else:
                            C+=1
                            self.expandCluster(position,neighborPixels,C)  
                    else:
                        self.pixelID[position]=-2 # pixel is zero! 
              arrayIterator.iternext()
        # consistency check
        sumVisited=self.pixelVisited.sum()
        if sumVisited != (self.imageSize*self.imageSize):
            print "DBSCAN: Not all pixels visited! Only ",sumVisited," out of ",  self.imageSize*self.imageSize  
        return
#---------------------------------------------------------------------------------          
    def expandCluster(self,position, neighborPixels, C):
        """ this function will expand a DBSCAN cluster, and modify neighborPixels"""
    
        if (self.pixelID[position] > 0) and (self.pixelID[position]!= C):
           print "About to Mark clustered point as being part of another cluster in expandCluster!" , self.pixelID[position], C
           # check to see that this point is NOT a core point 
           neighborPixelsPrime,neighborPixelsSum = self.regionQuery(position)
           print "neighborPixelSum is", neighborPixelsSum
        self.pixelID[position]=C   # add this point to cluster "C"
        lo_x=position[0]-int(self.eps)
        hi_x=position[0]+int(self.eps)+1
        lo_y=position[1]-int(self.eps)
        hi_y=position[1]+int(self.eps)+1
        # enforce boundaries of image:
        if lo_x <0 :
            lo_x = 0
        if hi_x > (self.imageSize-1):     
            hi_x = self.imageSize-1 
        if lo_y < 0:     
            lo_y = 0
        if hi_y > (self.imageSize-1):
            hi_y = self.imageSize-1   
        #arrayIterator=numpy.nditer(neighborPixels,flags=['multi_index'])
        arrayIterator=numpy.nditer(neighborPixels[lo_x:hi_x,lo_y:hi_y],flags=['multi_index'])
        while not arrayIterator.finished:
                        #positionPrime=arrayIterator.multi_index
                        #countsPrime=arrayIterator[0]
                        slicedPosition=arrayIterator.multi_index # this will return the indices of the SLICED array!
                        positionPrime=(lo_x+slicedPosition[0],lo_y+slicedPosition[1]) 
                        countsPrime=arrayIterator[0]
                        if not (self.pixelVisited[positionPrime]):  # new pixel, which may not be within range of the core pixel
                            if countsPrime:  # only do this for non-zero pixels <<My own logic>>, which are within range of the core pixel
                                self.pixelVisited[positionPrime]=True   #okay to mark as visited, as it is within range of the core pixel 
                                neighborPixelsPrime,neighborPixelsSum = self.regionQuery(positionPrime)
                                if neighborPixelsSum >= self.MinPts:
                                    # this point is a core point, mark it as a part of this cluster, and try to expand it
                                    self.expandCluster(positionPrime,neighborPixelsPrime,C)
                                else: 
                                    # this point is a edge point, mark it as a part of this cluster
                                    # note that the pixelID has not yet been set, as this point has not yet been visited 
                                    self.pixelID[positionPrime]=C
                            else: 
                                if self.imageArray[positionPrime] > 0: 
                                    pass # point is outside of range of core pixel, do nothing
                                else:
                                    # point is actually zero, mark as visited and as zero pixel
                                    self.pixelVisited[positionPrime]=True
                                    self.pixelID[positionPrime] = -2 
                        else:     # old pixel, which may not be within range of the core pixel 
                            if countsPrime: 
                                # this point is within range, and could be considered as a part of the cluster
                                if self.pixelID[positionPrime] > 0: # already a member of a cluster
                                  if self.pixelID[positionPrime] != float(C): # now a member of this cluster  
                                    self.pixelOverlaps[positionPrime]=C # need some more thought
                                    print "dbscan_analysis.expandCluster: Re-marking already ID'd pixel at ",positionPrime," which is a part of cluster", self.pixelID[positionPrime], " as a part of cluster ",C           
                                else:                               # should be a noise pixel
                                    self.pixelID[positionPrime]=C # mark this pixel as a part of the cluster 
                                
                            else:
                                if self.imageArray[positionPrime] > 0:
                                    pass # point is outside of range of core pixel, do nothing
                                else:
                                    pass # point is actually zero, it should have been marked as such and nothing else needs to be done. 
                        arrayIterator.iternext()
        #print "Leaving expandCluster ", C , neighborPixels.sum()                     
        return
#--------------------------------------------------------------------------------    
    def regionQuery(self,position):
        """ eps should be in units of pixels 
        """ 
        #create a new imageArray
        self.tempPixels*=0.
        neighborPixels = (self.tempPixels).copy()
        
        clusterSum=0.
        # setup bounds of a smaller, square array that contains every pixel in the neighborhood  
        lo_x=position[0]-int(self.eps)
        hi_x=position[0]+int(self.eps)+1
        lo_y=position[1]-int(self.eps)
        hi_y=position[1]+int(self.eps)+1
        # enforce boundaries of image:
        if lo_x <0 :
            lo_x = 0
        if hi_x > (self.imageSize-1):     
            hi_x = self.imageSize-1 
        if lo_y < 0:     
            lo_y = 0
        if hi_y > (self.imageSize-1):
            hi_y = self.imageSize-1   
        # now iterate though the neighborhood, and test for being within eps
        arrayIterator=numpy.nditer(self.imageArray[lo_x:hi_x,lo_y:hi_y],flags=['multi_index'])
        while not arrayIterator.finished:
                    countsPrime=arrayIterator[0]
                    if countsPrime: # only for non-zero elements
                        # only get indices for non-zero elements
                        slicedPosition=arrayIterator.multi_index # this will return the indices of the SLICED array!
                        positionPrime=(lo_x+slicedPosition[0],lo_y+slicedPosition[1]) 
                        distance=self.distanceQuery(position,positionPrime)
                        if distance <= self.eps:
                            #print "Adding ",positionPrime, " to cluster"
                            clusterSum+=countsPrime
                            neighborPixels[positionPrime]+=self.imageArray[positionPrime] # this pixel is within eps of the primary, so add it to the neighborPixels array
                    arrayIterator.iternext()          
        return neighborPixels,clusterSum
#---------------------------------------------------------------------------------
    def distanceQuery(self,position,positionPrime):
        """ get distance between pixels. This could be replaced with a lookup table  
        """
        r=numpy.asarray(position,dtype=float)
        rPrime=numpy.asarray(positionPrime,dtype=float)
        dr=r-rPrime
        radiusSquare=numpy.dot(dr,dr)
        radius=numpy.sqrt(radiusSquare) 
        return radius
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------
    def dbscanChecker(self,clusterID):
            """ used to confirm proper function of the dbscan code
            """
            inCluster=(self.pixelID==clusterID)
            sumCluster=0.
            sumPixels=0
            arrayIterator=numpy.nditer(self.imageArray,flags=['multi_index'])
            while not arrayIterator.finished:
               position=arrayIterator.multi_index
               counts=arrayIterator[0]
               if inCluster[position]:
                       sumPixels+=1
                       sumCluster+=counts                
               arrayIterator.iternext()
            print "dbscanChecker:",clusterID,sumPixels,inCluster.sum(),sumCluster,self.MinPts                           
            return
#---------------------------------------------------------------------------------------------------------------------------------------------

#==============================================================================================================================================
class dbscan_analysis:
      """ this class executes a DBscan clustering analysis to a greyscale image array

      """
      #------------------------------------------------------------------------------------------------------------------------------------------
      def __init__(self):
	  
	        return
	  #----------------------------------------------------------------------------
      def DoDBSCAN(self,minimumPoints,eps):
            self.db=dbscan_implementation(self.imageArray,minimumPoints,eps)
            return
      #---------------------------------------------------------------------------
      def ExploreClusters(self):
            """ this method prints out information on the clusters found in the DBSCAN analysis.
            """
            print "Exploring DBSCAN Clusters"
            arrayIterator=numpy.nditer(self.imageArray,flags=['multi_index'])
            while not arrayIterator.finished:
                    position=arrayIterator.multi_index
                    counts=arrayIterator[0]
                    if counts:
                        if self.db.pixelID[position] > 0:
                            print "      Cluster ID, position, counts = ",self.db.pixelID[position], position,counts
                    arrayIterator.iternext()      
            return  
      
      #---------------------------------------------------------------------------
      def AnalyzeResults(self):
            # get the number of points (actually counts) in the total data
            # get the number of clusters
            # get the number of points (actually counts) in the cluster
            # look at the distortion too
            
            foundClusters=False
            
            #self.ExploreClusters()
            
            # get zero pixels:
            self.zeroMask= (self.db.pixelID == -2)
            # get noise pixels:
            self.noiseMask= (self.db.pixelID  == -1)
            # get actual clusters
            self.maxClusterID=int(self.db.pixelID.max())
            
            # compute the level of background found
            backgroundCounts=(self.noiseMask*self.imageArray).sum()
            
            # now compute per cluster variables 
            if self.maxClusterID < 0:
                print "DBSCAN Found Zero Clusters"
                pass
            else:    
                foundClusters=True
                self.clusterMask=numpy.zeros((self.imageArray.shape[0],self.imageArray.shape[0],self.maxClusterID))
                self.clusterPixels=[]
                self.clusterCounts=[]
                self.clusterFrac=[]
                self.avgPixelCount=[]
                self.clusterPosition=[]
                self.clusterPositionVariance=[]
                self.clusterHottestPixel=[]
                for clusterID in range(self.maxClusterID):  # loop over all clusters found 
                    self.clusterMask[:,:,clusterID]= (self.db.pixelID  == clusterID+1)  # this produces a mask of pixels in a particular cluster
                    print "Cluster ", clusterID, " contains ", self.clusterMask[:,:,clusterID].sum(), " pixels and ", (self.clusterMask[:,:,clusterID]*self.imageArray).sum(), "counts"
                    self.clusterPixels.append(self.clusterMask[:,:,clusterID].sum())    # number of pixels in a cluster
                    self.clusterCounts.append((self.clusterMask[:,:,clusterID]*self.imageArray).sum()) # number of counts in a cluster
                    self.clusterFrac.append(self.clusterCounts[-1]/backgroundCounts)                       # number of counts in a cluster compared to identified background
                    self.avgPixelCount.append(self.clusterCounts[-1]/self.clusterPixels[-1])           # average pixel count in a cluster
                    pos,var = self.FindClusterPosition(clusterID)                                   # compute the weighted position and variance of the pixels in the cluster
                    self.clusterPosition.append(pos)
                    self.clusterPositionVariance.append(var)
                    self.clusterHottestPixel.append((self.clusterMask[:,:,clusterID]*self.imageArray).max())  # extract the position of the hottest pixel 
                totalpoints=self.noiseMask.sum() + self.clusterMask.sum()                              # this is the total number of pixels above threshold in this image 
            return foundClusters 
      
      #---------------------------------------------------------------------------
      def FindClusterPosition(self,clusterID):
          """ this will find the weighted average of the cluster position
          """
          # compute the imageArray of just the cluster 
          clusterArray=self.imageArray*self.clusterMask[:,:,clusterID]
          # now use the cluster_position class to do the computation
          positionInfo=cluster_position.cluster_position(clusterArray)
          # and get the info
          mean = positionInfo.mean
          variance = positionInfo.variance          
          # done, return
          return (mean,variance)
      #---------------------------------------------------------------------------
      def ChooseBestCluster(self):
            """ choose the best cluster to return 
            """
            maxCounts=0.
            minWidth=100000000. # large number
            bestID_counts=-1
            bestID_width=-1
            for clusterID in range(self.maxClusterID):  # loop over all clusters found
                # check counts 
                counts = self.clusterCounts[clusterID]
                if counts > maxCounts:
                    maxCounts=counts
                    bestID_counts=clusterID
                #check width, this code can be improved using numpy methods
                width_x=(self.clusterPositionVariance[clusterID])[0]
                width_y=(self.clusterPositionVariance[clusterID])[1]
                width_r=math.sqrt((width_x*width_x)+(width_y*width_y))
                relative_width=width_r/counts
                if relative_width < minWidth:
                    minWidth=relative_width
                    bestID_width=clusterID
            if bestID_counts==bestID_width:
                bestID=bestID_counts
            else:
                print "DBSCAN:ChooseBestCluster: can't find best cluster! Counts and width disagree!"
                bestID=bestID_counts   
            print "DBSCAN maxCounts:",maxCounts              
            return bestID            
      #---------------------------------------------------------------------------
      def GenerateOutput(self):
            """ load relevant results into standard output variables
            """
            numClustersArray=[self.maxClusterID for element in self.clusterCounts] 
            self.dbscanDict={
            'DBScan_NumPixels':self.clusterPixels,
            'DBScan_Counts':self.clusterCounts,
            'DBScan_ClusterFrac': self.clusterFrac,
            'DBScan_AvgPixelCount':self.avgPixelCount,
            'DBScan_PositionX': [element[0] for element in self.clusterPosition],
            'DBScan_PositionXVariance':   [element[0] for element in self.clusterPositionVariance],
            'DBScan_PositionY':[element[1] for element in self.clusterPosition],
            'DBScan_PositionYVariance':[element[1] for element in self.clusterPositionVariance],
            'DBScan_PeakHeight': self.clusterHottestPixel,
            'DBScan_NumClusters': numClustersArray
            }
            
            return
      #---------------------------------------------------------------------------
      def DoIt(self,inputArray,minimumPoints,eps):
            #self.clusterOutput=cluster_output.cluster_output()
            self.imageArray=inputArray
            self.DoDBSCAN(minimumPoints,eps) # run the DBSCAN algorithm
            self.foundClusters=self.AnalyzeResults() # get cluster info
            if self.foundClusters:
                # no longer worrying about the best cluster at this stage of analysis
                #self.bestClusterID=self.ChooseBestCluster() # out of the clusters found, pick the "best"
                self.GenerateOutput() # load results into the final observables
            return    
      #------------------------------------------------------------------------------         
      
