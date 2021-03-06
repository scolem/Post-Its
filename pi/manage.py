"""
Copyright 2014

   Scott Lemmer <scottlemmer1@gmail.com>
   Nelson Akoku Ebot Eno Akpa <akokuenow@gmail.com>

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

import cv2
import numpy as numpy
import glob
import json
from test import *
from issue import *
from issue import jsonconfig2str

config=jsonconfig2str()
f=open(config['picDirectory'] +'timelog.txt', 'r')

line=f.readline().strip()
line=f.readlines()
seclast=line[len(line)-2].strip()
last=line[len(line)-1].strip()
f.close()
#seclast=lines='';
#last=line='';

#while line:
#  seclast=last
#  last=line
#  line=f.readline().strip()


print 'comparing '+last+' and '+seclast
#list1 = glob.glob('day2/post?.jpg') + glob.glob('day2/post??.jpg')
#list2 = glob.glob('day1/post?.jpg') + glob.glob('day1/post??.jpg')
#list3 = glob.glob('day2/post?.json') + glob.glob('day2/post??.json')
#list4 = glob.glob('day1/post?.json') + glob.glob('day1/post??.json')

list1 = glob.glob(config['picDirectory'] +last+'/post*.jpg')
list2 = glob.glob(config['picDirectory'] +seclast+'/post*.jpg')
#print list2

checkRem=[0]*len(list2)
#print checkRem
def findAndTrack(list1,list2):
	sims = 0
	comps = 0
	for name1 in list1: # glob.glob('day2/post?.jpg'):
		name1= name1.replace('\\', '/')
		#print 'name1'+name1
		count = 0
		im1 = cv2.imread(name1)
		sign1 = grid_signature(binarize(im1))
		for name2 in list2:
			#print name2
			name2old=name2
			name2=name2.replace('\\', '/')
			im2 = cv2.imread(name2)
			sign2 = grid_signature(binarize(im2))
			comps +=1

			col1=json.load(open(name1[:-3] + 'json'))["type"]
			col2=json.load(open(name2[:-3] + 'json'))["type"]
			#print col1+col2
			if compare(sign1, col1, sign2, col2) == True:
##				print list2.index(name2old)
				checkRem[list2.index(name2old)]=1
				json_name1 = name1[:-3] + 'json' #day2
				json_name2 = name2[:-3] + 'json' #day1
				print json_name2
				print json_name1
				f1 = open(json_name2,'r')
				j1 = json.load(f1)
				col = j1["column"]

				f2 = open(json_name1,'r')
				j2 = json.load(f2)
				new_col = j2["column"]

				j2["issueID"]=j1["issueID"]
				with open(json_name1, "w") as jsonFile:
					jsonFile.write(json.dumps(j2))

				#print j2["issueID"]

				if col==new_col:
					print name2 + ' has not moved.'
				else:
					print name2 + ' has moved'
					print 'to move issue: '+j2["issueID"]+ str(col)+','+ str(new_col)
					moveIssue(j2["issueID"], str(col), str(new_col))

				count += 1
				sims +=1
		if count == 0:
			print name1 + ' is a new item'
			
			json_name1 = name1[:-3] + 'json'
			f2 = open(json_name1,'r')
			j2 = json.load(f2)
			new_col = j2["column"]

			print 'to newIssue: '+name1+','+str(new_col)

			newIssue(name1, str(new_col))
			
			f2.close()
		print '\n'

	for i in range (0, len(list2)):
##		print checkRem[i]
		if(checkRem[i]==0):
			print list2[i] + " was removed"
			
			json_name = list2[i][:-3] + 'json'
			f = open(json_name,'r')
			j = json.load(f)
			#new_col = j["column"]

			deleteIssue(j["issueID"])

findAndTrack(list1,list2)
	
