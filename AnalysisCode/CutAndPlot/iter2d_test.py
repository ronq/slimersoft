#! /usr/bin/env python
#
"""  A script for testing iteration over two ndarrays
     
     
     
"""
import sys

import math
import numpy
import scipy

a=numpy.arange(5)
b=numpy.arange(5,10)

for x,y in numpy.nditer([a,b]):
    print x, y

















