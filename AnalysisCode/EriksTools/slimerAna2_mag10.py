import Image
from threshold import *
#from skimage.filter import threshold_otsu
import sys
from ROOT import *
from pylab import *
from scipy import *
import numpy as np
from scipy import ndimage
from scipy import special
#import matplotlib.pyplot as plt	
from clusterAna2 import *
import os
import glob

#Generate root file with standard name
filename = sys.argv[1]
run = filename[filename.rfind("/")+1:filename.find(".tif")]
bkgfile = TFile(sys.argv[2])
numfiles = int(sys.argv[3])
numcurrent = int(sys.argv[4])
av_h = bkgfile.Get("average_hist")
stdev_h = bkgfile.Get("stdev_hist")

#extract data from picture into numpy array
x_size = 512
y_size = 512
X = range(x_size)
Y = range(y_size)
size = x_size*y_size
Z = range(size)
img = Image.open(filename)
pix = img.load()
tmp=[[pix[i,j] for i in X] for j in Y]
data = np.array(tmp,dtype=np.float)
averages = np.array([[av_h.GetBinContent(i+1,j+1) for i in X] for j in Y],dtype=np.float)
stdevs = np.array([[stdev_h.GetBinContent(i+1,j+1) for i in X] for j in Y],dtype=np.float)
data -= averages
out = ndimage.gaussian_filter(data, 7)
threshold = get_threshold(out)
#if threshold>10:
	#sys.exit(1)
data -= threshold[0]+3*threshold[1]
out -= threshold[0]+3*threshold[1]
out[out<0] = 0
#plt.imshow(out)
#plt.savefig('out')
#plt.close()

#Now I'll run the cluster algorithm 
outfile = TFile("rooted_"+run+".root","recreate")
h1 = TH1F("cluster_integral","",50000,0,50000)
h2 = TH1F("cluster_pixels","",x_size*y_size/100,0,x_size*y_size/100)
h3 = TH1F("cluster_smooth_integral","",50000,0,50000)
h4 = TH1F("cluster_smooth_pixels","",x_size*y_size/100,0,x_size*y_size/100)
h5 = TH1F("cluster_max","",1000,0,1000)
h6 = TH1F("cluster_smooth_max","",1000,0,1000)
h7 = TH1F("max","",1000,0,1000)
h8 = TH1F("thresholds","",numfiles,0,numfiles)
h8.Fill(numcurrent,threshold[1])

clusters = get_clusters(out,0.5*threshold[1])
for cluster in clusters:
	integral = 0
	count = 0
	smooth_integral = 0
	maximum = 0
	maximum_smooth = 0
	pixels = cluster.size
	for coord in cluster:
		smooth_integral+=out[coord[0]][coord[1]]
		if maximum < data[coord[0]][coord[1]]:
			maximum = data[coord[0]][coord[1]]
		if maximum_smooth < out[coord[0]][coord[1]]:
			maximum_smooth = out[coord[0]][coord[1]]
		if data[coord[0]][coord[1]]>0.5*threshold[1]:
			integral+=data[coord[0]][coord[1]]
			count+=1
	h1.Fill(integral)
	h2.Fill(count)
	h3.Fill(smooth_integral)
	h4.Fill(pixels)
	h5.Fill(maximum)
	h6.Fill(maximum_smooth)
	h7.Fill(data.max())
outfile.Write()
outfile.Close()
