from numpy import *
from scipy import optimize
from shaw_peakfind2 import *

def gaussian(mean, height, ro,  center_x, center_y, width_x, width_y):
    """Returns a gaussian function
    with the given parameters"""
    width_x = float(width_x)
    width_y = float(width_y)
    return lambda x,y: mean+height/(2*pi*width_x*width_y*sqrt(1-ro**2))*exp(-(((center_x-x)/width_x)**2-2*ro*(x-center_x)*(y-center_y)/(width_x*width_y)+((center_y-y)/width_y)**2)/2)

def moments(data, threshold):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution by calculating its
    moments """
    moments = findpeak(data,threshold)
    output = []
    for moment in moments:
        x = (moment[0].start+moment[0].stop-1)/2
        y = (moment[1].start+moment[1].stop-1)/2
        width_x = moment[0].stop-moment[0].start
        width_y = moment[1].stop-moment[1].start
        area = width_x*width_y
        data_of_interest = data[moment[0].start:moment[0].stop+1,moment[1].start:moment[1].stop+1]
        in_cluster = data_of_interest > threshold
        if area>10:
            #non_zero_col = (col > threshold)
            #non_zero_row = (row > threshold)
            #i = x
            #j = y
            #while non_zero_row[i] or non_zero_col[j]:
            #   if i+2==512:
            #       i = x
            #       break
            #   if j+2==512:
            #       j = y
            #       break
            #   if non_zero_row[i+1]:
            #       i+=1
            #   if non_zero_col[j+1]:
            #       j+=1
            #   if not non_zero_row[i+1]:
            #       i+=1
            #   if not non_zero_col[j+1]:
            #       j+=1
            #i-=1
            #j-=1
            #if pi*(i-x)*(i-y)>10:
            #print "Hello"
            out = np.argwhere(in_cluster)
            out += [moment[0].start, moment[1].start]
            too_much = np.argwhere(out==511)
            too_little = np.argwhere(out==0)
            #print too_much
            #print too_little
            height = data[x][y]*2*pi*width_x*width_y
            if (out.size/2>100) and (out.size/2<25000) and len(too_much)==0 and len(too_little)==0:
                #print "Hello"
                output.append((0,height,0,x,y,width_x,width_y))
    return output

def fitgaussian(data,threshold):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution found by a fit"""          
    params = moments(data,threshold)
    print params
    errorfunction = lambda p: ravel(gaussian(*p)(*indices(data.shape))-data)
    output = []
    for moment in params:
        print "input",errorfunction,moment
        #for element in moment:
        #    print element, type(element)
        p, success = optimize.leastsq(errorfunction, moment)
        print "output",errorfunction,moment
        output.append(p)
    return output
