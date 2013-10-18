class cluster_position:
    """ This is a class for determining the position and shape of clusters. It is assumed that the data input is an array with weights. 
    """
    #-------------------------------------------------------------------------------------
    def __init__(self,inputData):
        self.inputData=inputData
        self.normData=ComputeNormalizedData(inputData)
        self.mean, self.covariance = ComputeClusterPosition(self.normData)
        self.variance=[self.covariance[0,0],self.covariance[1,1]]
        return
    #------------------------------------------------------------------------------------
    def ComputeNormalizedData(self,inputData):
        """ this will normalize an array of weights
        """
        inputDataSum=numpy.sum
        if inputDataSum: # check against division by zero 
            normData=inputData/inputDataSum
        else:
            normData=inputData*0.
        return normData    
    #-------------------------------------------------------------------------------------
    def ComputeClusterPosition(self,clusterArray):
        """ this will compute the weighted average of the cluster position

        'clusterArray' should be normalized
                                                                                                                                
        note that the means can be computed by just multiplying the clusterArray with row or column vectors like [0,1,2....] and then taking the sum                                                 
                                                                                                                                                                                                           
        """
        # setup variables first     
        mean=[0.,0.]
        covariance=numpy.zeros((2,2))
        countsSquared=0.0

        # Compute the mean. Do this quickly by using projections -------------------------------------                                                                                                    
        # project in two dimensions                                                                                                                                                                       
        projectX=numpy.sum(clusterArray,axis=1) # note the ordering of the axis here!                                                                                                                     
        projectY=numpy.sum(clusterArray,axis=0)

        # compute the means from the projections                                                                                                                                                          
        # get mean x                                                                                                                                                                                      
        arrayIterator=numpy.nditer(projectX,flags=['multi_index'])
        while not arrayIterator.finished:
            position=arrayIterator.multi_index # this will return the indices of the SLICED array!                                                                                                    
            counts=arrayIterator[0]
            if counts:
                mean[0]+=float(position[0])*counts
            arrayIterator.iternext()
        # get mean y                                                                                                                                                                                      
        arrayIterator=numpy.nditer(projectY,flags=['multi_index'])
        while not arrayIterator.finished:
            position=arrayIterator.multi_index # this will return the indices of the SLICED array!                                                                                                    
            counts=arrayIterator[0]
            if counts:
                mean[1]+=float(position[0])*counts  # note the indexing of the position array: this is correct                                                                                        
            arrayIterator.iternext()

        # mean has been computed    
        # now compute the covariance matrix-------------------------------------------------------------                                                                                                  
        arrayIterator=numpy.nditer(clusterArray,flags=['multi_index'])
        while not arrayIterator.finished:
            position=arrayIterator.multi_index # this will return the indices of the SLICED array!                                                                                                    
            counts=arrayIterator[0]
            if counts:
                countsSquared+=counts*counts
                covariance[0,0]+=counts* (float(position[0])-mean[0])*(float(position[0]-mean[0]))
                covariance[0,1]+=counts* (float(position[0])-mean[0])*(float(position[1]-mean[1]))
                covariance[1,1]+=counts* (float(position[1])-mean[1])*(float(position[1]-mean[1]))
            arrayIterator.iternext()
            
        covariance[1,0] =  covariance[0,1]
        covarianceFactor=1./(1.-countsSquared) # because we've already normalized                                                                                                                         
        
        covariance=covariance*covarianceFactor
        variance=[covariance[0,0],covariance[1,1]]

        return (mean,covariance)
    #-------------------------------------------------------------------------------------------------




