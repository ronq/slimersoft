import pandas
import string
import numpy
import ROOT
class plot_pandas:
    """ This is a class for ploting PANDAS information 
    """
    #------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self,df,pairs2D):
	    """A class for quick plotting of variables inside PANDAS DataFrames. This will book and fill a histogram for each variable in the DataFrame. 
	    """
	    self.histoArray=[]  # array of histogram objects 
	    self.numBins=1000
	    # loop over all columns in dataFrame
	    dfIterator=df.iteritems()
	    for variableName, seriesData in dfIterator:  # variableName is the label of the column in the DataFrame, while seriesData.values will produce the actual values 
	        if seriesData.dtype != numpy.dtype(object): # don't plot paths to images 
	            self.BookAndFillHistogram(variableName,seriesData.values)
	    return   
    #-------------------------------------------------------------------------------------------------------------------------------------------
    def BookAndFillHistogram(self,label,data):
        """This method will book,fill and write to disk a histogram for each call. 
        """
        # extract upper and lower limits
        isNonsense=(data != -999.) # find elements which are just initialized
        upper_limit=numpy.amax(data)   
        lower_limit=numpy.amin(data*isNonsense) # will result in the lower limit being zero
        # book histogram, using label as the ROOT name and title
        newHisto=ROOT.TH1F(label,label, self.numBins, lower_limit, upper_limit)
        # now fill histogram
        dataIterator=numpy.nditer(data) # get an iterator for the ndarray holding the data 
        while not dataIterator.finished:
            newHisto.Fill(dataIterator[0])    # fill the histogram
            dataIterator.iternext()
        newHisto.Write()                      # write the histogram to the ROOT file. Through the magic of the PyROOT binding, there's no need to reference the file here!
        return








