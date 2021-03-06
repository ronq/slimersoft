#! /usr/bin/env python
#
"""  This script will test some features of PANDAS DataFrames 

     Extra text
     
     usage:  datafrane_tests.py
     
     
     
"""
import sys

import math
import numpy
import scipy
import Image

import pandas


hdf5FileName="dataframe_tests_hdf5.h5"
store=pandas.HDFStore(hdf5FileName,'w')  

a={'ImageSum':[400,500,600],'ImageMean':[50,30,20]}
b={'X':[30,10,55],'Y':[10,30,70]}
print a
print b
a.update(b)
print a

#a['ImageSum'].extend([700,800,900])
testindex=['test_index','test_index','test_index']
#testindex=['test_index']
print a
    
#df=pandas.DataFrame.from_dict(a,index=testindex)    
df=pandas.DataFrame(a,index=testindex)
"""      
df=pandas.DataFrame({'ImagePath': self.output_fullFilePath,
                                 'ImageMax' : self.output_imageMax,
                                 'ImageMean': self.output_imageMean,
                                 'ImageVariance':           self.output_imageVariance,
                                 'ImageSum':                self.output_imageSum,
                                 'HotPixels1Sigma':         self.output_hotpixels1Sigma,
                                 'HotPixels2Sigma':         self.output_hotpixels2Sigma,
                                 'HotPixels3Sigma':         self.output_hotpixels3Sigma,
                                 'HotPixels4Sigma':         self.output_hotpixels4Sigma,
                                 'HotPixels5Sigma':         self.output_hotpixels5Sigma,
                                 'DBScan_NumPixels':        [result.clusterOutput.outputClusterSize for result in self.output_dbscan_results],
                                 'DBScan_Counts':           [result.clusterOutput.outputCounts for result in self.output_dbscan_results],
                                 'DBScan_ClusterFrac':      [result.clusterOutput.outputClusterFrac for result in self.output_dbscan_results],
                                 'DBScan_AvgPixelCount':    [result.clusterOutput.outputAvgPixelCount for result in self.output_dbscan_results],
                                 'DBScan_PositionX':         [result.clusterOutput.outputPosition[0] for result in self.output_dbscan_results],
                                 'DBScan_PositionXVariance': [result.clusterOutput.outputPositionVariance[0] for result in self.output_dbscan_results],
                                 'DBScan_PositionY':         [result.clusterOutput.outputPosition[1] for result in self.output_dbscan_results],
                                 'DBScan_PositionYVariance': [result.clusterOutput.outputPositionVariance[1] for result in self.output_dbscan_results],
                                 'DBScan_PeakHeight':       [result.clusterOutput.outputPeakHeight for result in self.output_dbscan_results],
                                 'DBScan_NumClusters':      [result.clusterOutput.outputNumberOfClusters for result in self.output_dbscan_results],
                                 'kmeans_NumPixels':        [result.clusterOutput.outputClusterSize for result in self.output_kmeans_results],
                                 'kmeans_Counts':           [result.clusterOutput.outputCounts for result in self.output_kmeans_results],
                                 'kmeans_ClusterFrac':      [result.clusterOutput.outputClusterFrac for result in self.output_kmeans_results],
                                 'kmeans_AvgPixelCount':    [result.clusterOutput.outputAvgPixelCount for result in self.output_kmeans_results],
                                 'kmeans_PositionX':         [result.clusterOutput.outputPosition[0] for result in self.output_kmeans_results],
                                 'kmeans_PositionXVariance': [result.clusterOutput.outputPositionVariance[0] for result in self.output_kmeans_results],
                                 'kmeans_PositionY':         [result.clusterOutput.outputPosition[1] for result in self.output_kmeans_results],
                                 'kmeans_PositionYVariance': [result.clusterOutput.outputPositionVariance[1] for result in self.output_kmeans_results],
                                 'kmeans_PeakHeight':       [result.clusterOutput.outputPeakHeight for result in self.output_kmeans_results],
                                 'kmeans_NumClusters':      [result.clusterOutput.outputNumberOfClusters for result in self.output_kmeans_results]
                                 })                    
"""
#print df['test_index']
print df
#now I need to figure out how to modify the contents, so I can append elements to the array associated with 'key'


store.append('ImageData',df) # this will make a table, which can be appended to
store.close()             

