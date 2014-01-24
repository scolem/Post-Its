"""
Copyright 2014

   Scott Lemmer <scottlemmer1@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from test import *
import os
import time
from changetime import makeTime
from issue import jsonconfig2str
import shutil

config=jsonconfig2str()

def getfileDir():
  #get file directory
  f=open(config['picDirectory'] +'timelog.txt', 'r+')
#  line=f.readline()
  lines=f.readlines()
  last=lines[len(lines)-1]
#  while line:
#    last=line
#    line=f.readline()

##  print jsonconfig2str()['picDirectory']
##  print last
  filedir=config['picDirectory'] + str(last) + "/"
  f.close()
  return filedir

def countDots():
  original = cv2.imread(filedir+'pic.jpg')

  hsv_im = cv2.cvtColor(original,cv2.COLOR_BGR2HSV)
  YELLOW_MIN = np.array([20, 70, 60],np.uint8)
  YELLOW_MAX = np.array([35, 255, 255],np.uint8)
  yellow_threshed = cv2.inRange(hsv_im, YELLOW_MIN, YELLOW_MAX)
  yellow_threshed = cv2.medianBlur(yellow_threshed,71)	
  #cv2.imwrite('yellow_edges.jpg',yellow_threshed)

  contours, hierarchy = cv2.findContours(yellow_threshed,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  noDots = 0
  for cnt in contours:
      
      approx1 = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)

      #print cv2.contourArea(cnt)
      if cv2.contourArea(cnt) > 1000:
          noDots += 1

  return noDots

def remLastLine(file):
  print 'removing picture'
  readFile=open('timelog.txt')
  lines=readFile.readlines()
  readFile.close()

  w=open('timelog.txt', 'w')
  w.writelines([item for item in lines[:-2]])
  w.write(lines[len(lines)-2].rstrip())
  w.close()

  shutil.rmtree(file)

print 'starting program'
#create new file to process in and update timelog
makeTime()
filedir=getfileDir()
print filedir

#take picture
print 'taking picture'
os.system('raspistill -o '+filedir+'pic.jpg')

#Check number of dots
numDots=countDots()
print 'Number of dots found: '+str(numDots)
# jsonconfig2str()['noCols']

if numDots == config['noCols']*2+2:
  print 'Correct number of dots'

  #take second picutre
  print 'taking second picture'
  os.system('raspistill -o '+filedir+'pic1.jpg')

  im1 = image_preprocessing(filedir+'pic.jpg')
  im2 = image_preprocessing(filedir+'pic1.jpg')

  compare= compare(grid_signature(im1), grid_signature(im2))

  if compare:
      print'pictures match'

      #crop image
      from crop import *
      
      #manage images
      from manage import *
  else:
      print'pictures do not match'
      remLastLine(filedir)

else:
  print 'Incorrect number of dots'
  remLastLine(filedir)
print 'ending program'
