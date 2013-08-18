import Image
from threshold import *
import sys
from ROOT import *
from pylab import *
from scipy import *
import numpy as np
from scipy import ndimage
from scipy import special
import matplotlib.pyplot as plt	
from fit import *
from calculations import *
import os
import glob

#Generate root file with standard name
filename = sys.argv[1]
run = filename[filename.rfind("/")+1:filename.find(".tif")]
bkgfile = TFile(sys.argv[2])
outfile = TFile("rooted_"+run+".root","recreate")
av_h = bkgfile.Get("average_hist")
stdev_h = bkgfile.Get("stdev_hist")

#extract data from picture into numpy array
x_size = 512
y_size = 512
two_sigma_val = 0.0215392793
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
out -= threshold[0]+3*threshold[1]
data -= threshold[0]+3*threshold[1]
out[out<0] = 0

#plt.imshow(out)
#plt.savefig('out')
#plt.close()

#Now I'll run the fit 
h1 = TH1F("integrate_fit","",100000,0,100000)
h2 = TH1F("integrate_pixels","",15000,0,15000)
h3 = TH1F("peakh_fit","",200,0,200)
h4 = TH1F("peakh_pixels","",200,0,200)
h5 = TH1F("peaka_fit","",15000,0,15000)
h6 = TH1F("peaka_pixels","",15000,0,1500)
h7 = TH1F("raw_pixel_integral","",100000,0,100000)
h8 = TH1F("raw_pixel_area","",15000,0,15000)
#h9 = TH1F("fixed_integral","",100000,0,100000)
percent = special.erf(sqrt(2))
params = fitgaussian(out,0.5*threshold[1])
for p in params:
	fit = gaussian(*p)
	results = np.array([[fit(j,i) for i in X] for j in Y],dtype=np.float)
	coords = np.argwhere((results-p[0])/p[1]>two_sigma_val/(p[5]*p[6]))
	integral = 0
	smooth_integral = 0
	num_pix = 0
	num_smooth_pix = len(coords)
	for coord in coords:
		smooth_integral += out[coord[0]][coord[1]]
		if data[coord[0]][coord[1]]>0.5*threshold[1]:
			integral += data[coord[0]][coord[1]]
			num_pix += 1
	h1.Fill(abs(2*pi*p[1]*p[5]*p[6]*percent*percent))
	h2.Fill(smooth_integral)
	h3.Fill(p[1])
	h4.Fill(out[int(p[3])][int(p[4])])
	h5.Fill(abs(pi*p[5]*p[6]))
	h6.Fill(num_smooth_pix)
	h7.Fill(integral)
	h8.Fill(num_pix)
	#p0 = [mean]
	#plt.imshow(results)
	#plt.savefig('out{}.png'.format(i))
	#plt.close()
bkgfile.Close()
outfile.Write()
outfile.Close()
