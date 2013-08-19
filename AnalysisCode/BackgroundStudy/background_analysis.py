#! /usr/bin/env python
#
"""  This script will analyze background runs and look at statistics 

     Extra discription
     
     usage:  background_analysis.py  [path to images to display]  [root name of output file]
     
     
     
"""
import sys
import math
import numpy
import scipy
import scipy.stats
import glob
import os
import Image
import ROOT
import pandas    
    
#-------------------------
def GetRun(fileName):
        baseName=fileName.split(".")[0] # removes file extension
        baseNameComponents=baseName.split("t") # splits baseName up using "t" as the delimiter
        run=int(baseNameComponents[-1]) # we want the last element, as a integer
        return run
#-------------------------    


# get arguments
inputFiles=glob.glob(sys.argv[1])
outputRootName=sys.argv[2]

# create ROOT file for histogram output, and book histograms 
outputROOTFileName=outputRootName + ".root"
newfile=ROOT.TFile(outputROOTFileName,'RECREATE') 


pixelCount=ROOT.TH1I('pixelCount','pixelCount', 1000, 400, 1400)
pixelCountHigh=ROOT.TH1I('pixelCountHigh','pixelCountHigh', 65000, 1400, 66400)

imageModePlot=ROOT.TH1F('imageMode','imageMode', 1000, 400., 600.)
imageMeanPlot=ROOT.TH1F('imageMean','imageMean', 1000, 400., 600.)
imageSTDPlot=ROOT.TH1F('imageSTD','imageSTD', 1000, 0., 100.)
imageMaxPlot=ROOT.TH1I('imageMax','imageMax', 65536, 0, 65536)
imageMedianPlot=ROOT.TH1F('imageMedian','imageMedian', 1000, 400., 600.)


imageMode=[]
imageMean=[]
imageSTD=[]
imageMedian=[]
imageMax=[]
runNumber=[]
print "Processing ", len(inputFiles), " images"
for inputFile in inputFiles:
        pil_im=Image.open(inputFile)
        #inputData_raw=numpy.array(pil_im.getdata()).reshape(pil_im.size[0], pil_im.size[1])
        inputData_raw=numpy.array(pil_im.getdata()).reshape(-1)
        # convert to floats !!!!!!!!!!!!!!!
        # extract number of run 
        thisRunNumber=GetRun(inputFile)
        runNumber.append(thisRunNumber)
        imageMean.append(numpy.mean(inputData_raw))              # compute mean
        imageSTD.append(numpy.std(inputData_raw))                # compute STD
        imageMedian.append(numpy.median(inputData_raw))          # compute median
        vals, counts = scipy.stats.mode(inputData_raw,axis=None) # compute mode
        imageMode.append(vals[0])                                 
        imageMax.append(numpy.amax(inputData_raw))               # max 
        
        
        # now histogram the pixel counts 
        
        pixelIterator=numpy.nditer(inputData_raw)  # get an iterator for the ndarray holding the data 
        while not pixelIterator.finished:
           pixelCount.Fill(pixelIterator[0])
           pixelCountHigh.Fill(pixelIterator[0])
           pixelIterator.iternext()
           
# now histogram the statistics of the images
for index in range(len(inputFiles)):        
    imageModePlot.Fill(imageMode[index])
    imageMeanPlot.Fill(imageMean[index])
    imageSTDPlot.Fill(imageSTD[index])
    imageMaxPlot.Fill(imageMax[index])
    imageMedianPlot.Fill(imageMedian[index])
        
# now convert to PANDAS format and save to HDF5 databases
hdf5FileName=outputRootName +"_hdf5.h5"
store=pandas.HDFStore(hdf5FileName,'w')
df=pandas.DataFrame({'ImagePath': inputFiles,
                                 'RunNumber': runNumber,   
                                 'ImageMax' : imageMax,
                                 'ImageMean': imageMean,
                                 'ImageSTD':  imageSTD,
                                 'ImageMedian': imageMedian,
                                 'ImageMode': imageMode
                    })             
store.append('BackgroundImageData',df) # this will make a table, which can be appended to
store.close()

newfile.Write()  # write all histograms to disk, redundant?
newfile.Close()


