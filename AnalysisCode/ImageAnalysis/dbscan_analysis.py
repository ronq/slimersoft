#! /usr/bin/env python
#
import numpy
import sklearn
import sklearn.cluster
#import scipy
#import scipy.cluster
#import scipy.cluster.vq
import math


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
                        if not (self.pixelVisited[positionPrime]):
                            self.pixelVisited[positionPrime]=True
                            if countsPrime:  # only do this for non-zero pixels <<My own logic>>
                                neighborPixelsPrime,neighborPixelsSum = self.regionQuery(positionPrime)
                                #print neighborPixelsSum
                                if neighborPixelsSum >= self.MinPts:
                                    # i think I need to call expandCluster again here, starting from positionPrime
                                    # or perhaps I simply can't slice the neighbor matrix
                                    self.expandCluster(positionPrime,neighborPixelsPrime,C)
                                    #neighborPixels+=neighborPixelsPrime  # need to make sure I'm not double counting pixels here
                                #if not (self.pixelID[positionPrime]): 
                                #    self.pixelID[positionPrime]=C  
                            else:
                                if not (self.pixelID[positionPrime]): 
                                    self.pixelID[positionPrime]=-2 # zero pixel 
                        if self.pixelID[positionPrime] <= 0:   # not a part of a cluster
                            if self.pixelID[positionPrime] > -2:   # not a zero pixel
                               #if self.pixelID[positionPrime] == 0:
                                    #print "Marking Already visited non-noise pixel as being part of a cluster" # if this never shows up, I can change the above logic to "pixelID==-1, then..."
                               self.pixelID[positionPrime]=C    # pixel is marked as part of this cluster
                        """
                        else: # pixel has already been visited 
                            if self.pixelID[positionPrime] == -1:  # if the point is zero, it has already been marked as a zero point and pixelID=-2
                                                                   # if the point is already a member of a cluster, pixelID > 0
                                                                   # if point has already been visited, pixelID != 0                                          
                                                                   # so the point must have been marked as noise, and should be changed
                                    self.pixelID[positionPrime]=C  # mark this point as belonging to the cluster
                        """
                        arrayIterator.iternext()
        #print "Leaving expandCluster ", C , neighborPixels.sum()                     
        return
#--------------------------------------------------------------------------------    
    def regionQuery(self,position):
        """ eps should be in units of pixels 
        """ 
        #create a new imageArray
        self.tempPixels*=0.
        neighborPixels = self.tempPixels
        
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
                    slicedPosition=arrayIterator.multi_index # this will return the indices of the SLICED array!
                    positionPrime=(lo_x+slicedPosition[0],lo_y+slicedPosition[1]) 
                    countsPrime=arrayIterator[0]
                    if countsPrime: # only for non-zero elements
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
                #print "DBSCAN Found Zero Clusters"
                pass
            else:    
                print "DBSCAN Found ",self.maxClusterID, " clusters"
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
                    #print "Cluster ", clusterID, " contains ", self.clusterMask[:,:,clusterID].sum(), " pixels and ", (self.clusterMask[:,:,clusterID]*self.imageArray).sum(), "counts"
                    self.clusterPixels.append(self.clusterMask[:,:,clusterID].sum())    # number of pixels in a cluster
                    self.clusterCounts.append((self.clusterMask[:,:,clusterID]*self.imageArray).sum()) # number of counts in a cluster
                    self.clusterFrac.append(self.clusterCounts/backgroundCounts)                       # number of counts in a cluster compared to identified background
                    self.avgPixelCount.append(self.clusterCounts[-1]/self.clusterPixels[-1])           # average pixel count in a cluster
                    pos,var = self.ComputeClusterPosition(clusterID)                                   # compute the weighted position and variance of the pixels in the cluster
                    self.clusterPosition.append(pos)
                    self.clusterPositionVariance.append(var)
                    self.clusterHottestPixel.append((self.clusterMask[:,:,clusterID]*self.imageArray).max())  # extract the position of the hottest pixel 
                totalpoints=self.noiseMask.sum() + self.clusterMask.sum()                              # this is the total number of pixels about threshold in this image 
                """
                print self.clusterFrac
                print self.clusterPixels
                print self.clusterCounts
                print self.avgPixelCount
                print self.clusterHottestPixel
                print self.clusterPosition
                print self.clusterPositionVariance
                """
             
            """
            totalpoints=self.features.size/2. # each point is 2x1
            clusterLabelsFound=[]   # this is the number of clusters +1 (for noise)
            clusterPointsFound=[]   # this is the energy estimate for the cluster 
            for pointLabel in labels:       # loop over all point labels
                if pointLabel not in clusterLabelsFound:   # check if this label (cluster) is new
                    clusterLabelsFound.append(pointLabel)     # if so add it to the list of clusters 
                clusterPointsFound[clusterLabelsFound.index(pointLabel)]+=1    # another point(count) in this cluster
                     
            self.clustersFound=len(clusterLabelsFound) - (-1 in clusterLabelsFound) # -1 denotes noise
            
            if ( -1 in clusterLabelsFound ):
                self.backgroundEvents=clusterPointsFound[clusterLabelsFound.index(-1)]
            else:
                self.backgroundEvents=0    
            
            # now setup other variables for later analysis:
            
            self.backgroundCounts=0
            self.clusterCounts=[]
            self.clusterLabels=[]  
            for i in range(len(clusterPointsFound)):
                if clusterLabelsFound[i]==-1:
                    self.backgroundCounts=clusterPointsFound[i]
                else:
                    self.clusterLabels.append(clusterLabelsFound[i])    
                    self.clusterCounts.append(clusterPointsFound[i])
            
            self.backgroundFrac=self.backgroundCounts/totalpoints
            self.clusterToTotalFrac=[]
            self.clusterToBackgroundFrac=[]
            for counts in self.clusterCounts:
                    self.clusterToTotalFrac.append(counts/totalpoints)
                    self.clusterToBackgroundFrac.append(counts/backgroundCounts)
            """
            return
      #---------------------------------------------------------------------------
      def ComputeClusterPosition(self,clusterID): 
            """ this will compute the weighted average of the cluster position
            """
            clusterArray=self.imageArray*self.clusterMask[:,:,clusterID]
            # compute the mean position first
            arrayIterator=numpy.nditer(clusterArray,flags=['multi_index'])
            mean=[0.,0.]
            variance=[0.,0.]
            while not arrayIterator.finished:
                    position=arrayIterator.multi_index # this will return the indices of the SLICED array!
                    counts=arrayIterator[0]
                    mean[0]+=float(position[0])*counts/(self.clusterCounts[clusterID-1])
                    mean[1]+=float(position[1])*counts/(self.clusterCounts[clusterID-1])
                    arrayIterator.iternext() 
            # then the standard deviation
            res=[0.,0.]
            arrayIterator.reset()
            while not arrayIterator.finished:
                    position=arrayIterator.multi_index # this will return the indices of the SLICED array!
                    counts=arrayIterator[0]
                    res[0]=float(position[0])-mean[0]
                    res[1]=float(position[1])-mean[1]
                    variance[0]+=(res[0]*res[0])*counts/(self.clusterCounts[clusterID-1])
                    variance[1]+=(res[1]*res[1])*counts/(self.clusterCounts[clusterID-1])
                    arrayIterator.iternext() 
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
                    bestID=clusterID
                #check width, this code can be improved using numpy methods
                width_x=(self.clusterPositionVariance[clusterID])[0]
                width_y=(self.clusterPositionVariance[clusterID])[1]
                width_r=math.sqrt((width_x*width_x)+(width_y*width_y))
                relative_width=width_r/counts
                if relative_width < minWidth:
                    minWidth=relative_width     
                    
                     
      #---------------------------------------------------------------------------
      def DoIt(self,inputArray,minimumPoints,eps):
            self.imageArray=inputArray
            self.DoDBSCAN(minimumPoints,eps) # run the DBSCAN algorithm
            # check for a second cluster
            self.AnalyzeResults() # get cluster info
            self.ChooseBestCluster() # out of the clusters found, pick the "best"
            #print "DBSCAN Results:", self.backgroundFrac,self.clusterToTotalFrac,self.clusterToBackgroundFrac
            
            return    
      #------------------------------------------------------------------------------         
      
