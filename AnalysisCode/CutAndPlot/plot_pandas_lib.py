import pandas
import string
import numpy
import ROOT
class plot_pandas:
    """ This is a class for ploting PANDAS information 
    """
    #------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self,rootFile,df,pairs):
	    
	    self.histoArray=[]  # array of histogram objects 
	    self.numBins=1000
	    # loop over all columns in dataFrame
	    dfIterator=df.iteritems()
	    #print dfIterator
	    for variableName, seriesData in dfIterator:
	        #print variableName
	        #print seriesData.values
	        if seriesData.dtype != numpy.dtype(object): # don't try to plot the 
	            self.BookAndFillHistogram(variableName,seriesData.values)
	    """
	    while not dfIterator.finished:
	        print dfIterator[0]
	    #for column in df.iteritems()
	            # extract the data and book and fill a histogram
	        dfIterator.iternext()    
	    """
	    return   
    #-------------------------------------------------------------------------------------------------------------------------------------------
    def BookAndFillHistogram(self,label,data):
        # extract upper and lower limits
        isNonsense=(data != -999.)
        upper_limit=numpy.amax(data)
        lower_limit=numpy.amin(data*isNonsense) # will result in the lower limit being zero
        print label,lower_limit,upper_limit
        # book histogram
        newHisto=ROOT.TH1F(label,label, self.numBins, lower_limit, upper_limit)
        # now fill histogram
        dataIterator=numpy.nditer(data)
        while not dataIterator.finished:
            newHisto.Fill(dataIterator[0])
            dataIterator.iternext()
        newHisto.Write()     
        return








