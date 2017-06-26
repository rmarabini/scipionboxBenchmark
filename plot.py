import collections
import glob
import os
import time
import sys


from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--inputfile", dest="filename",
                  help="input  FILE")

(options, args) = parser.parse_args()
if options.filename:
   print "filename", options.filename

#acces popstcript

exit(1)

d = collections.OrderedDict()

searchedfile = glob.glob("GRID_0?/DATA/Images-Disc?/GridSquare_*/Data/*_frames*.mrc")
#searchedfile = glob.glob("20160930_CSM_AdDELTA7/GRID_0?/DATA/Images-Disc?/GridSquare_*/Data/*_frames*.mrc")
files = sorted( searchedfile, key = lambda file: os.path.getctime(file))

previousT = 0
x=[]
y=[]
counter = 0
for file in files:
    T = os.path.getctime(file)
    interval = T -  previousT
    print file, interval
    previousT = T
    x.append(counter)
    y.append(interval)
    counter += 1

#print x, y


import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as font_manager

#t = np.arange(0.0, 2.0, 0.01)
#s = 1 + np.sin(2*np.pi*t)
f = plt.figure()
plt.semilogy(x, y, linewidth=2.5)

plt.xlabel('Movie #')
plt.ylabel('Creation Time (sec)')
plt.title('Movie Production Interval')
plt.grid(True)
plt.savefig("test.png")
plt.savefig("test.pdf")
plt.show()

#histogram
#n, bins, patches = plt.hist(y, 50, normed=1, facecolor='green', alpha=0.75)
plt.hist(y, bins=5)
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
plt.show()

