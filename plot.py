import collections
import glob
import os
import time
import sys
import sqlite3 as lite


from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--inputfile", dest="filename",
                  help="input  FILE")
parser.add_option("-l", "--labels", dest="labels",
                  help="labels to display")
parser.add_option("-d", "--minId", dest="minId",
                  help="start at this id", type="int", default=1)
parser.add_option("-D", "--maxID", dest="maxId",
                  help="end at this id", type="int", default=1000000)

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
    plt.plot(timeValues, data[key], linewidth=2.5, label=key)

plt.xlabel('Movie #')
plt.ylabel('Creation Time (sec)')
plt.title('Movie Production Interval')
plt.grid(True)
#plt.legend(loc='best')
plt.legend(loc=2).get_frame().set_alpha(0.5)
##plt.savefig("test.png")
##plt.savefig("test.pdf")
plt.show()


