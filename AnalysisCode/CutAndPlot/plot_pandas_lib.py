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
	    self.numBins=1000
	    # loop over all columns in dataFrame for 1D plotting
	    dfIterator=df.iteritems()
	    for variableName, seriesData in dfIterator:  # variableName is the label of the column in the DataFrame, while seriesData.values will produce the actual values 
	        if seriesData.dtype != numpy.dtype(object): # don't plot paths to images 
	            self.BookAndFillHistogram(variableName,seriesData.values)
	    # now loop over the entries in pairs2D for 2D plotting 
	    for pair in pairs2D:
	        data1=df[pair[0]].values # get data for first variable in pair
	        data2=df[pair[1]].values # get data for the second variable in pair
	        # call the 2D histogram plotting routine
	        self.BookAndFill2DHistogram(pair[0],pair[1],data1,data2)
	    return   
    #---------------------------------------------------------------------------
    def GetLimits(self,data):
        """ compute lower and upper limits for a histogram given the data to be plotted
        """
        # extract upper and lower limits
        isNonsense=(data != -999.) # find elements which are just initialized
        upper_limit=numpy.amax(data)   
        lower_limit=numpy.amin(data*isNonsense) # will result in the lower limit being zero
        return lower_limit, upper_limit
    #-------------------------------------------------------------------------------------------------------------------------------------------
    def BookAndFillHistogram(self,label,data):
        """This method will book,fill and write to disk a histogram for each call. 
        """
        lower_limit, upper_limit = self.GetLimits(data)
        # book histogram, using label as the ROOT name and title
        newHisto=ROOT.TH1F(label,label, self.numBins, lower_limit, upper_limit)
        # now fill histogram
        dataIterator=numpy.nditer(data) # get an iterator for the ndarray holding the data 
        while not dataIterator.finished:
            newHisto.Fill(dataIterator[0])    # fill the histogram
            dataIterator.iternext()
        newHisto.Write()                      # write the histogram to the ROOT file. Through the magic of the PyROOT binding, there's no need to reference the file here!
        return
    #-------------------------------------------------------------------------------------------------------------------------------------------
    def BookAndFill2DHistogram(self,label1,label2,data1,data2):
        """This method will book,fill and write to disk a histogram for each call. 
        """
        # get limits first
        lower_limit1, upper_limit1 = self.GetLimits(data1)
        lower_limit2, upper_limit2 = self.GetLimits(data2)
        # book histogram, using label as the ROOT name and title
        label=label2+"_versus_"+label1
        newHisto=ROOT.TH2F(label,label, self.numBins, lower_limit1, upper_limit1,self.numBins,lower_limit2, upper_limit2)
        newHisto.GetXaxis().SetTitle(label1)
        newHisto.GetYaxis().SetTitle(label2)
        # now fill histogram
        for datum1,datum2 in numpy.nditer([data1,data2]): # get an iterator for the ndarrays holding the data 
            newHisto.Fill(datum1,datum2)                 # fill the histogram
        newHisto.Write()                                 # write the histogram to the ROOT file. Through the magic of the PyROOT binding, there's no need to reference the file here!
        return
    #-------------------------------------------------------------------------------------------------------------------------------------------------

