#! /usr/bin/env python
#
"""  This script will analyze Numpy array formatted images to compare the averages of a couple of data sets 

     Extra discription
     
     usage:  background_average.py  [path to images to average] [base file name for output] 
     
     
     
"""
import sys
import math
import numpy
import scipy
import glob
import matplotlib.pyplot
import matplotlib.backends.backend_pdf


nbins=100

pdfOutput=matplotlib.backends.backend_pdf.PdfPages


# get arguments
inputList=glob.glob(sys.argv[1])
outputRoot=sys.argv[2]

#plotRange=[400,1000]
plotRange=[400,65535]

#nbins=plotRange[1]-plotRange[0]
nbins=100
pdfOutput=matplotlib.backends.backend_pdf.PdfPages(outputRoot)

for npzfile in inputList:
    inputArray=(numpy.load(npzfile))['imageArray']
    data=numpy.reshape(inputArray,-1)  # need to format the numpyArray as a single dimension?
    print len(data)
    #data=numpy.array([500,510,520,480,480,480,480,500])
    #n, bins, patches = matplotlib.pyplot.hist(data,bins=nbins,histtype='stepfilled')
    # at this point, the data are integers. Check for values beyond 10000
    #isLarge=data > 10000
    #numLarge=numpy.sum(isLarge)
    #if numLarge:
    #    print numLarge, " pixels above 10000"
         
    n, bins, patches = matplotlib.pyplot.hist(data,bins=nbins,histtype='step',range=plotRange)
    matplotlib.pyplot.xlabel("Pixel Count")
    matplotlib.pyplot.ylabel("Number of Pixels")
    matplotlib.pyplot.title("Histogram of Pixel Counts in Dataset")
    #matplotlib.pyplot.yscale('log')
    matplotlib.pyplot.semilogy()
    #x1,x2,y1,y2 = matplotlib.pyplot.axis()
    #matplotlib.pyplot.axis((400,65535,1.0,y2))
    matplotlib.pyplot.savefig(pdfOutput,format="pdf")
    #matplotlib.pyplot.show()
    #pdfOutput.savefig()
    #raw_input("Press Enter To Continue")
pdfOutput.close()


# form list of npz files
# for each file
#    compute the average for all pixels for all images
#    compute the STD for all pixels for all images
#    print out the results 




