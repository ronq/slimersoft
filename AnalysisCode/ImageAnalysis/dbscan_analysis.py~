#! /usr/bin/env python
#
import numpy
import sklearn
import sklearn.cluster
#import scipy
#import scipy.cluster
#import scipy.cluster.vq
class dbscan_implementation:
#------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self,image):
        self.MinPts=100
        self.imageSize=image.shape[0] # assume it is square
        self.eps = 80.0 # must be a float!!!!!
        self.pixelID=numpy.zeros((512,512))  # this marks each point in an image with a particular ID, either zero (-2) noise (-1) or a cluster (positive integer)
        self.pixelVisited=numpy.zeros((512,512))
        self.tempPixels=numpy.zeros((self.imageSize,self.imageSize)) # for internal use only
        self.imageArray=image
        self.dbscan() 
        return
#-----------------------------------------------------------------------------------------------------------   
    def dbscan(self):
        print "Beginning DBScan"
        C=0 # this marks the cluster number
        self.MinPts =10 # this is actually the minimum sum of COUNTS
        self.imageSize=512
        arrayIterator=numpy.nditer(self.imageArray,flags=['multi_index'])
        while not arrayIterator.finished:
                    position=arrayIterator.multi_index
                    counts=arrayIterator[0]
                    self.pixelVisited[position]=True
                    if counts: # don't try to find a cluster when the pixel is zero <<this is my own logic!>>
                        neighborPixels,neighborPixelsSum  = self.regionQuery(position) # neighborPixels will be a copy of the imageArray, with all but the neighbor pixels masked
                        #print neighborPixels.sum(),neighborPixelsSum
                        if neighborPixelsSum < self.MinPts:
                            self.pixelID[position] = -1  #mark this position as noise
                        else:
                            C+=1
                            # C denotes a new cluster
                            print "Found new cluster, calling expandCluster"
                            self.expandCluster(position,neighborPixels,C)  
                    else:
                        self.pixelID[position]=-2 # pixel is zero! 
                    arrayIterator.iternext()       
        print "Done with DBScan"
        return
#---------------------------------------------------------------------------------          
    def expandCluster(self,position, neighborPixels, C):
        """ this function will expand a DBSCAN cluster, and modify neighborPixels"""
    
        self.pixelID[position]=C   # add this point to cluster "C"
        arrayIterator=numpy.nditer(neighborPixels,flags=['multi_index'])
        while not arrayIterator.finished:
                        positionPrime=arrayIterator.multi_index
                        countsPrime=arrayIterator[0]
                        if not (self.pixelVisited[position]):
                            self.pixelVisited[position]=True
                            if countsPrime:  # only do this for non-zero pixels <<My own logic>>
                                neighborPixelsPrime,neighborPixelsSum = self.regionQuery(positionPrime)
                                if neighborPixelsSum >= self.MinPts:
                                    neighborPixels+=neighborPixelsPrime  # need to make sure I'm not double counting pixels here
                                if not (self.pixelID[position]): 
                                    self.pixelID[position]=C  
                            else:
                                if not (self.pixelID[position]): 
                                    self.pixelID[position]=-2 # zero pixel 
                        arrayIterator.iternext()         
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
                    positionPrime=arrayIterator.multi_index
                    countsPrime=arrayIterator[0]
                    if countsPrime: # only for non-zero elements
                        distance=self.distanceQuery(position,positionPrime)
                        if distance <= self.eps:
                            print "Adding ",positionPrime, " to cluster"
                            clusterSum+=countsPrime
                            neighborPixels[positionPrime]+=self.imageArray[positionPrime] # this pixel is within eps of the primary, so add it to the neighborPixels array
                            print neighborPixels[positionPrime],countsPrime,clusterSum,positionPrime
                    arrayIterator.iternext()          
                    
        """ 
        # this uses bounds on a larger array, to prevent from slicing the array. This is likely slower though, so don't use this method
        # setup bounds of a smaller, square array that contains every pixel in the neighborhood  
        lo_x=position[0]-int(self.eps)
        hi_x=position[0]+int(self.eps)
        lo_y=position[1]-int(self.eps)
        hi_y=position[1]+int(self.eps)
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
        arrayIterator=numpy.nditer(self.imageArray,flags=['multi_index'])
        while not arrayIterator.finished:
                    countsPrime=arrayIterator[0]
                    if countsPrime: # only for non-zero elements
                        positionPrime=arrayIterator.multi_index
                        if positionPrime[0] >= lo_x: 
                            if positionPrime[0] <= hi_x: # don't add 1 here
                                if positionPrime[1] >= lo_y:
                                    if positionPrime[1] <= hi_y: # don't add 1 here 
                                        distance=self.distanceQuery(position,positionPrime)
                                        if distance <= self.eps:
                                            print "Adding ",positionPrime, " to cluster"
                                            clusterSum+=countsPrime
                                            neighborPixels[positionPrime]=self.imageArray[positionPrime] # this pixel is within eps of the primary, so add it to the neighborPixels array
                    arrayIterator.iternext()        
        """
        
        return neighborPixels,clusterSum
#---------------------------------------------------------------------------------
    def distanceQuery(self,position,positionPrime):
        """ get distance between pixels 
        """
        #print "Running distanceQuery on: ",position
        #r=numpy.array(position,dtype=float)
        #rprime=numpy.array(positionPrime,dtype=float)
        #dr=numpy.array(position-positionPrime,dtype=float) # .astype(float) may be faster
        r=numpy.asarray(position,dtype=float)
        rPrime=numpy.asarray(positionPrime,dtype=float)
        dr=r-rPrime
        radiusSquare=numpy.dot(dr,dr)
        #radiusSqaure=num.square(dr) # could be faster
        radius=numpy.sqrt(radiusSquare)  # should look for numpy function if possible
        return radius
#---------------------------------------------------------------------------------
class dbscan_analysis:
      """ this class executes a DBscan clustering analysis to a greyscale uint16 array

      """
      #------------------------------------------------------------------------------------------------------------------------------------------
      def __init__(self):
	  
	  return
      
      #---------------------------------------------------------------------------- 
      def ComputeCenterOfEnergy(self):
            return
      #---------------------------------------------------------------------------  
      def DoDBSCAN(self):
            self.db=dbscan_implementation(self.imageArray)
            # debug code
            #print centers, distortion
            #print numpy.shape(code), numpy.sum(code)
            return
      #---------------------------------------------------------------------------
      def AnalyzeResults(self):
            # get the number of points (actually counts) in the total data
            # get the number of clusters
            # get the number of points (actually counts) in the cluster
            # look at the distortion too
            # get zero pixels:
            self.zeroMask= (self.db.pixelID == -2)
            # get noise pixels:
            self.noiseMask= (self.db.pixelID  == -1)
            
            # get actual clusters
            self.maxClusterID=int(self.db.pixelID.max())
            
            print "DBSCAN Found ",self.maxClusterID+1, " clusters"
            self.clusterMask=numpy.zeros((self.imageArray.shape[0],self.imageArray.shape[0],self.maxClusterID+1))
            for clusterID in range(self.maxClusterID):
                self.clusterMask[:,:,clusterID]= (self.db.pixelID  == clusterID)
                print "Cluster ", clusterID, " contains ", self.clusterMask[:,:,clusterID].sum(), " pixels and ", (self.clusterMask[:,:,clusterID]*self.imageArray).sum(), "counts"
            
            totalpoints=self.noiseMask.sum() + self.clusterMask.sum()
            checkpoints=totalpoints+self.zeroMask.sum()
            
            backgroundCounts=(self.noiseMask*self.imageArray).sum()
            print "Background: ",backgroundCounts
            print "    Totalpoints and Checkpoints:  ",totalpoints, checkpoints,512*512
            
            
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
      
      
      #---------------------------------------------------------------------------
      def DoIt(self,inputArray):
            self.imageArray=inputArray
            self.DoDBSCAN() # run the DBSCAN algorithm
            # check for a second cluster
            self.AnalyzeResults() # get cluster info
            #print "DBSCAN Results:", self.backgroundFrac,self.clusterToTotalFrac,self.clusterToBackgroundFrac
            
            return    
      #------------------------------------------------------------------------------         
      
