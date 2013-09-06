#!/usr/bin/env python
#
""" This will make two pretty plots: an overlay plot and a ratio plot  
"""

import ROOT
import math
import glob
import sys


samples=["/proj/Slimer/SlimerAnalysis/background_study/shutter_open_9_3_2013_200msec_background_analysis.root",
"/proj/Slimer/SlimerAnalysis/background_study/shutter_closed_9_3_2013_200msec_background_analysis.root",
"/proj/Slimer/SlimerAnalysis/background_study/scope_off_9_3_2013_200msec_background_analysis.root"]
legendText=["Camera Shutter Open",
            "Camera Shutter Closed",
            "Microscope Hub Off"]




#fillStyles=[3001,3002,3002,3002]
#fillStyles=[1001,3017,3018,3002]
fillStyles=[1001,3001,3001,3001]
fillColors=[40,8,4,2]


#open a canvas
plot_canvas = ROOT.TCanvas('custom','Cut Plot' ,1)  # open a Canvas (needed for plot) (use 2 for sqaure)
#plot_canvas.Divide(1,2)       # split into two
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gPad.SetLogy( 1 ) 


histogram_name="pixelCount"
rebinFactor=1.0
plotRange=[400.,700.]
xTitle="Pixel Counts (arbitrary)"
yTitle="# events/counts"

files=[ROOT.TFile(sample) for sample in samples]
# get the histograms
plots=[rootFile.Get(histogram_name) for rootFile in files]
print plots

# now draw the plots
for plot in plots:
    plot.Rebin(rebinFactor)
    if plot == plots[0]:  # first plot
        plot.Draw("HIST")    
        plot.GetXaxis().SetRangeUser(plotRange[0],plotRange[1])
        legend=ROOT.TLegend(0.6,0.9,0.40,1.00)
        # set titles here
        plot.GetXaxis().SetTitle(xTitle) 
        plot.GetYaxis().SetTitle(yTitle)
    else:
        plot.Draw("HISTSAME")        
        # scale here
    legend.AddEntry(plot,legendText[plots.index(plot)],"lpf")
    plot.SetFillStyle(fillStyles[plots.index(plot)])
    plot.SetFillColor(fillColors[plots.index(plot)])
    plot.SetLineColor(fillColors[plots.index(plot)])
legend.Draw("SAME")
raw_input("Press Enter to continue iteration")
plot_canvas.Print("lightLeak_overlay.pdf")
plot_canvas.Print("lightLeak_overlay.png")

# now do ratio plot 
ROOT.gPad.SetLogy( 0 ) 
ratio=plots[0].Clone()    # make a copy of plot1 
ratio.SetName("RatioPlot")
ratio.Draw()
ratio.Sumw2()          # needed to handle errors 
#print ratio, plots
ratio.Divide(plots[1],plots[0],1.0,1.0,'')   # divide histograms
#ratio.Draw("E")                        # plot ratio
#plots[0].Divide(plots[1])
#plots[0].Draw("E")
#ratio.SetMaximum(4.0)
#ratio.SetMinimum(0.25)
raw_input("Press Enter to continue iteration")
plot_canvas.Print("lightLeak_ratio.pdf")
plot_canvas.Print("lightLeak_ratio.png")













