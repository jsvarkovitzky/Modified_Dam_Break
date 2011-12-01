
"""
Module to create topo for this example.
Piecewise linear composite beach and solitary wave.

"""
import sys
from pyclaw.geotools import topotools
import numpy as np


def generatetopo(test):
    print "Generating topography for landslide."

    nxpoints = 10000
    nypoints = 6
    xlower = -1000.
    xupper = 1000.
    dx = (xupper-xlower)/(nxpoints-1)
    ylower = 0.
    yupper = (nypoints-1)*dx
    slope = 0.1
    
    def maketopo():
       """
       Output topography file for the entire domain
       """
       outfile= "landslide.topotype2"     
       topotools.topo2writer(outfile,topo,xlower,xupper,ylower,yupper,nxpoints,nypoints)
       

    def topo(x,y):
        """
        Linear Slope
        """
        z = np.where(x>xlower, slope*x,0)  
        return z
    
    maketopo()

if __name__=='__main__':
    if len(sys.argv) > 1:
        generatetopo(sys.argv[1])
    else:
        generatetopo("A")
