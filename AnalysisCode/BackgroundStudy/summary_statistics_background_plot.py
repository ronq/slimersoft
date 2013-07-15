#! /usr/bin/env python
#
"""  This script will plot the summary statistics arrays in the image array npz files

     Extra discription
     
     usage:  summary_statistics_background_plot.py  [path to npz files to analyze] [base file name for output] 
     
     
     
"""
import sys
import math
import numpy
import scipy
import glob
import matplotlib.pyplot
import matplotlib.backends.backend_pdf
import osq

nbins=100

pdfOutput=matplotlib.backends.backend_pdf.PdfPages


# get arguments
inputList=glob.glob(sys.argv[1])
outputRoot=sys.argv[2]

#plotRange=[400,1000]
#nbins=plotRange[1]-plotRange[0]

arraySelectors=['imageSums','imageMeans','imageSTDs','imageMaxes','imageHotPixels']
#outputFileName=outputRoot+"_"+arraySelector+".pdf"
outputFileName=outputRoot+".pdf"
pdfOutput=matplotlib.backends.backend_pdf.PdfPages(outputFileName)

for npzfile in inputList:
   for arraySelector in arraySelectors: 
    fileRootName=os.path.basename(npzfile)
    inputArray=(numpy.load(npzfile))[arraySelector]
    data=numpy.reshape(inputArray,-1)  # nned to format the numpyArray as a single dimension?
    print len(data)
    #data=numpy.array([500,510,520,480,480,480,480,500])
    #n, bins, patches = matplotlib.pyplot.hist(data,bins=nbins,histtype='stepfilled')
    #n, bins, patches = matplotlib.pyplot.hist(data,bins=nbins,normed=1,histtype='step',range=plotRange)
    #n, bins, patches = matplotlib.pyplot.hist(data,normed=1,histtype='stepfilled')
    n, bins, patches = matplotlib.pyplot.hist(data,histtype='stepfilled')
    matplotlib.pyplot.xlabel(arraySelector)
    matplotlib.pyplot.ylabel("Number of Counts")
    matplotlib.pyplot.title("Data From "+fileRootName)
    #matplotlib.pyplot.yscale('log')
    #matplotlib.pyplot.semilogy()
    matplotlib.pyplot.savefig(pdfOutput,format="pdf")
    #matplotlib.pyplot.show()
    #pdfOutput.savefig()
    #raw_input("Press Enter To Continue")
    matplotlib.pyplot.clf()
    """
    print "Mean from ",fileRootName, " = ",numpy.mean(data),"+/-",numpy.std(data)," and max ",numpy.amax(data)
    for element in data:
        if element > 1000.:
            print element
        if element < 0.:
            print element    
    """
pdfOutput.close()


# form list of npz files
# for each file
#    compute the average for all pixels for all images
#    compute the STD for all pixels for all images
#    print out the results 




