import datetime
import os

timestamp=datetime.datetime.now().strftime('%y%m%d%H')
print timestamp
myfile=open("timelog.txt", "a")
myfile.write("\n"+timestamp)
myfile.close()

try:
    os.mkdir(timestamp)
except OSError:
    print "Error: The file already exists"
