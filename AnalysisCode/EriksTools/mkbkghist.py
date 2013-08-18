import Image
import sys
from ROOT import *
from pylab import *
from scipy import *
import numpy as np
from scipy import ndimage
from scipy import special
import matplotlib.pyplot as plt	
from gaussfitter import *
from calculations import *
import os
import glob

#Generate root file with standard name
dirname = sys.argv[1]
date = sys.argv[2]
outfile = TFile("proc_background_"+date+".root","recreate")
filenames = glob.glob(dirname+"*")
#extract data from picture into numpy array
x_size = 512
y_size = 512
size = x_size*y_size
Z = range(size)
n = len(filenames)
h1 = TH2F("average_hist","",512,0,512,512,0,512)
h2 = TH2F("stdev_hist","",512,0,512,512,0,512)
h3 = TH1F("averages","",n,0,n)
h4 = TH1F("stdevs","",n,0,n)
h5 = TH1F("Bkg spectrum","",10000,0,1000)
x=[[0 for i in range(x_size)] for j in range(y_size)]
tmp1 = np.array(x,dtype=np.float)
tmp2 = np.array(x,dtype=np.float)
index = 0
for filename in filenames:
	print filename
	img = Image.open(filename)
	pix = img.load()
	x=[[pix[i,j] for i in range(x_size)] for j in range(y_size)]
	data = np.array(x,dtype=np.float)
	tmp1 += data
	mean = ndimage.mean(data)
	stdev = ndimage.standard_deviation(data)
	h3.Fill(index,mean)
	h4.Fill(index,stdev)
	index += 1

tmp1 /= n
[h1.Fill(i%x_size,i/x_size,tmp1[i%x_size][i/x_size]) for i in Z]
[h5.Fill(tmp1[i%x_size][i/x_size]) for i in Z]
for filename in filenames:
	print filename
	img = Image.open(filename)
	pix = img.load()
	x=[[pix[i,j] for i in range(x_size)] for j in range(y_size)]
	data = np.array(x,dtype=np.float)
	tmp2 += (data-tmp1)*(data-tmp1)
	
tmp2 /= n
[h2.Fill(i%x_size,i/x_size,sqrt(tmp2[i%x_size][i/y_size])) for i in Z]
outfile.Write()
outfile.Close()
