import collections
import glob
import os
import time
import sys
import sqlite3 as lite
#scipion python plot.py -i cp_movies.sqlite3 -l "eth1_recv disk_write"
# ~/Scipion/scipion_box/scipion python ./plot.py -i 32_frames_correlation_netbackup_diskbackup.sqlite -o netbackup  -l "eth1_recv disk_write gpuUse_0 eth0_send disk_read" -t "32 frames motioncorr2 net backup" -x "time (minutes)" -y "MB/sec or percentage" -d 310 -D 410

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--inputfile", dest="filename",
                  help="input  FILE")
parser.add_option("-o", "--outfile", dest="outFilename",
                  help="output  FILE")
parser.add_option("-l", "--labels", dest="labels",
                  help="labels to display")
parser.add_option("-d", "--minId", dest="minId",
                  help="start at this id", type="int", default=1)
parser.add_option("-D", "--maxID", dest="maxId",
                  help="end at this id", type="int", default=1000000)
parser.add_option("-t", "--title", dest="title", help="plot Title")
parser.add_option("-x", "--X", dest="xlabel", help="label x axis")
parser.add_option("-y", "--Y", dest="ylabel", help="label y axis")
parser.add_option("-s", "--semiLogScale", action="store_true", dest="log", default=False,
                  help="logarithm plot")
(options, args) = parser.parse_args()

tableName = "log"
conn = lite.connect(options.filename, isolation_level=None)
cur = conn.cursor()
cur.execute("select julianday(timestamp)  from %s where id=%d" %
                    (tableName,  options.minId))
initTime = cur.fetchone()[0]

cur.execute("""select (julianday(timestamp) - %f)*24.*60.  
               from %s 
               where id>=%d and id <=%d""" % 
               (initTime, tableName,  options.minId,  options.maxId ))

timeValues = [r[0] for r in cur.fetchall()]

#id INTEGER, 
#timestamp DATE,
#cpu FLOAT,
#mem FLOAT,
#swap FLOAT,
#gpuMem_0 FLOAT,
#gpuUse_0 FLOAT,
#gpuTem_0 FLOAT,
#eth1_send FLOAT,
#eth1_recv FLOAT,
#disk_read FLOAT,
#disk_write FLOAT
color={}
color['eth1_recv']="blue"
color['disk_write']="green"
color['gpuUse_0']="red"
#color['eth0_send']="magenta"
#color['disk_read']="cyan"
color['eth0_send']="magenta"
color['disk_read']="cyan"
#y: yellow
#k: black
#w: white
data = {}
def get(name):
    try:
        cur.execute("""select %s 
                       from %s 
                       where id>=%d and id <=%d""" % (name, tableName, options.minId,  options.maxId ))
    except Exception as e:
        print("ERROR readind data (plotter). I continue")
    return [r[0] for r in cur.fetchall()]

for key in options.labels.split():
    data[key] = get(key)


#print x, y


import matplotlib.pyplot as plt
f = plt.figure()
for key in options.labels.split():
    if options.log:
        _data = [x+1 for x in data[key]]
        plt.semilogy(timeValues, _data, linewidth=2.5, label=key, color=color[key])
    else:    
        plt.plot(timeValues, data[key], linewidth=2.5, label=key, color=color[key])

plt.xlabel(options.xlabel)
plt.ylabel(options.ylabel)
plt.title(options.title)
plt.grid(True)
#plt.legend(loc='best')
plt.legend(loc=2).get_frame().set_alpha(0.5)
plt.savefig("%s.jpg"%options.outFilename)
plt.savefig("%s.pdf"%options.outFilename)
plt.show()


