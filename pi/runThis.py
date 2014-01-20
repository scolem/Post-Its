""" Copyright 2014
   Scott Lemmer<scottlemmer1@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License."""

from test import *
import os
import time
from changetime import makeTime
from issue import jsonconfig2str

#create new file to process in and update timelog
makeTime()

#get file directory
f=open(jsonconfig2str()['picDirectory'] +'timelog.txt', 'r+')
line=f.readline()

while line:
  last=line
  line=f.readline()

filedir=jsonconfig2str()['picDirectory'] + str(last) + "/"
print filedir

take pictures
os.system('raspistill -o '+filedir+'pic.jpg')
time.sleep(5)
os.system('raspistill -o '+filedir+'pic1.jpg')

im1 = image_preprocessing(filedir+'pic.jpg')
im2 = image_preprocessing(filedir+'pic1.jpg')

compare= compare(grid_signature(im1), grid_signature(im2))

print compare

if compare:
    print 'run program'

    #crop image
    #from crop import *
    
    #manage image
    #from manage import *
else:
    print 'don\'t run'
