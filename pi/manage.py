import cv2
import numpy as numpy
import glob
import json
from test import *
from issue import *

f=open('timelog.txt', 'r')

line=last=f.readline().strip()

seclast='';

while line:
  seclast=last
  last=line
  line=f.readline().strip()


print last
print seclast
#list1 = glob.glob('day2/post?.jpg') + glob.glob('day2/post??.jpg')
#list2 = glob.glob('day1/post?.jpg') + glob.glob('day1/post??.jpg')
#list3 = glob.glob('day2/post?.json') + glob.glob('day2/post??.json')
#list4 = glob.glob('day1/post?.json') + glob.glob('day1/post??.json')

list1 = glob.glob(last+'/post*.jpg')
list2 = glob.glob(seclast+'/post*.jpg')

checkRem=[0]*len(list2)

def findAndTrack(list1,list2):
	sims = 0
	comps = 0
	for name1 in list1: # glob.glob('day2/post?.jpg'):
		#print name1
		count = 0
		im1 = cv2.imread(name1)
		sign1 = grid_signature(binarize(im1))
		for name2 in list2:
			#print name2
			im2 = cv2.imread(name2)
			sign2 = grid_signature(binarize(im2))
			comps +=1
			if compare(sign1,sign2) == True:
				print list2.index(name2)
				checkRem[list2.index(name2)]=1
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

				print j2["issueID"]

				if col==new_col:
					print name2 + ' has not moved.'
				else:
					print name2 + ' has moved'
					
					moveIssue(j2["issueID"], str(col), str(new_col))

					print 'move issue'+j2["issueID"]+ str(col)+ str(new_col)

				count += 1
				sims +=1
		if count == 0:
			print name1 + ' is a new item'
			
			json_name1 = name1[:-3] + 'json'
			f2 = open(json_name1,'r')
			j2 = json.load(f2)
			new_col = j2["column"]

			print 'to newIssue '+name1+str(new_col)

			newIssue(name1, str(new_col))
			
			f2.close()
		print '\n'

	for i in range (0, len(list2)):
		print checkRem[i]
		if(checkRem[i]==0):
			print list2[i] + " was removed"
			
			json_name = list2[i][:-3] + 'json'
			f = open(json_name,'r')
			j = json.load(f)
			#new_col = j["column"]

			deleteIssue(j["issueID"])
	print sims	
	print comps

def manage():
  f=open('timelog.txt', 'r')

  line=last=f.readline().strip()

  seclast='';

  while line:
    seclast=last
    last=line
    line=f.readline().strip()



  #list1 = glob.glob('day2/post?.jpg') + glob.glob('day2/post??.jpg')
  #list2 = glob.glob('day1/post?.jpg') + glob.glob('day1/post??.jpg')
  #list3 = glob.glob('day2/post?.json') + glob.glob('day2/post??.json')
  #list4 = glob.glob('day1/post?.json') + glob.glob('day1/post??.json')

  list1 = glob.glob(last+'/post*.jpg')
  list2 = glob.glob(seclast+'/post*.jpg')

  checkRem=[0]*len(list2)

  findAndTrack(list1,list2)

  print 'done'

manage()

	
