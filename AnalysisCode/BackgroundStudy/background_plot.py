#! /usr/bin/env python
#
"""  This script will analyze Numpy array formatted images in order to plot a histogram of pixel counts 

     Extra discription
     
     usage:  background_plot.py  [path to images to average] [base file name for output] 
     
     
     
"""
import sys
import math
import numpy
import scipy
import glob
import matplotlib.pyplot
import matplotlib.backends.backend_pdf
import os

nbins=100

pdfOutput=matplotlib.backends.backend_pdf.PdfPages


# get arguments
inputList=glob.glob(sys.argv[1])
outputRoot=sys.argv[2]

#plotRange=[400,1000]
#plotRange=[400,65535]
plotRange=[400,10000]
plotRange=[400,1000]
#nbins=plotRange[1]-plotRange[0]
nbins=100
pdfOutput=matplotlib.backends.backend_pdf.PdfPages(outputRoot)

for npzfile in inputList:
    fileRootName=os.path.basename(npzfile)
    print "Loading ",fileRootName
    inputArray=(numpy.load(npzfile,mmap_mode='r'))['imageArray']
    data=numpy.reshape(inputArray,-1)  # need to format the numpyArray as a single dimension
    print len(data)
    n, bins, patches = matplotlib.pyplot.hist(data,bins=nbins,histtype='step',range=plotRange)
    matplotlib.pyplot.xlabel("Pixel Count")
    matplotlib.pyplot.ylabel("Number of Pixels")
    matplotlib.pyplot.title("Data From "+fileRootName)
    #matplotlib.pyplot.yscale('log')
    matplotlib.pyplot.semilogy()
    matplotlib.pyplot.savefig(pdfOutput,format="pdf")
    #matplotlib.pyplot.clf()
    #matplotlib.pyplot.show()
    #pdfOutput.savefig()
    #raw_input("Press Enter To Continue")
pdfOutput.close()


# form list of npz files
# for each file
#    compute the average for all pixels for all images
#    compute the STD for all pixels for all images
#    print out the results 




