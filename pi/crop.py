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

import numpy as np
import cv2
from test import *
import json
import math
from issue import jsonconfig2str
#import test as t

f=open(jsonconfig2str()['picDirectory'] +'timelog.txt', 'r+')
line=f.readline()

while line:
  last=line
  line=f.readline()


filedir=jsonconfig2str()['picDirectory'] + str(last) + "/"
#print filedir

noCols=jsonconfig2str()['noCols']

#Return the angle in degrees
def angle(row_diff, col_diff):
  ratio = float(row_diff) / float(col_diff)
  ang_rad = math.atan(ratio)
  ang_deg = math.degrees(ang_rad)
  return ang_deg

#issueID image must not be skew by 45 degrees or more.
def rotateImage(image, angel):#parameter angel in degrees
    height = image.shape[0]
    width = image.shape[1]
    image_center = (width/2, height/2)#rotation center
    rot_mat = cv2.getRotationMatrix2D(image_center,angel, 1.0)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result


def rotateYellows(image):
	hsv_im = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
	YELLOW_MIN = np.array([20, 70, 60],np.uint8)
	YELLOW_MAX = np.array([35, 255, 255],np.uint8)
	yellow_threshed = cv2.inRange(hsv_im, YELLOW_MIN, YELLOW_MAX)
	yellow_threshed = cv2.medianBlur(yellow_threshed,71)
	#cv2.imwrite(filedir+'yellow_dots.jpg',yellow_threshed)

	contours, hierarchy = cv2.findContours(yellow_threshed,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	yellows = np.zeros((noCols*2+2,2),dtype = float)
	my_rows = np.zeros(noCols*2+2,dtype = float)
	i = 0
	for cnt in contours:
		if cv2.contourArea(cnt)> 1000 and i<noCols*2+2:
			#print cv2.contourArea(cnt)
			M = cv2.moments(cnt)
			col,row = float(M['m10']/M['m00']), float(M['m01']/M['m00'])
			my_rows[i] = row
			yellows[i,0] = row
			yellows[i,1] = col
			i = i+1

	#-----------------------------------------------------------------
	#print my_rows
	my_rows.sort()
	height = my_rows[noCols*2+2-1]-my_rows[0]
	#print height
	percentage = 0.05*height
	top_rows = my_rows[0:noCols+1:]
	top_rows_diff = top_rows.max() - top_rows.min()
	#print 'toprowsdiff = ' + str(top_rows_diff)

	#-----------------------------------------------------------------

	minrow_index = yellows[0:noCols*2+2: , 0:1:].argmin()
	maxrow_index = yellows[0:noCols*2+2: , 0:1:].argmax()
	mincol_index = yellows[0:noCols*2+2: , 1::].argmin()
	maxcol_index = yellows[0:noCols*2+2: , 1::].argmax()

	minrow = yellows[minrow_index,0]
	col4minrow = yellows[minrow_index,1]

	maxrow = yellows[maxrow_index,0]
	col4maxrow = yellows[maxrow_index,1]

	mincol = yellows[mincol_index,1]
	row4mincol = yellows[mincol_index,0] 

	maxcol = yellows[maxcol_index,1]
	row4maxcol = yellows[maxcol_index,0]

	ang = 0

	if top_rows_diff<percentage:
		rot_im = image
	#Rotate anti-clockwise
	elif col4minrow < col4maxrow:
		row_diff = abs(row4maxcol-minrow)
		col_diff = abs(maxcol-col4minrow)
		ang = angle(row_diff,col_diff)
		rot_im = rotateImage(image, ang)

	#Rotate clockwise
	else:
		row_diff = abs(minrow-row4mincol)
		col_diff = abs( col4minrow - mincol)
		ang = angle(row_diff,col_diff)
		rot_im = rotateImage(image, -ang)
	
	return rot_im
	

def column(original):
	hsv_im = cv2.cvtColor(original,cv2.COLOR_BGR2HSV)
	YELLOW_MIN = np.array([20, 70, 60],np.uint8)
	YELLOW_MAX = np.array([35, 255, 255],np.uint8)
	yellow_threshed = cv2.inRange(hsv_im, YELLOW_MIN, YELLOW_MAX)
	yellow_threshed = cv2.medianBlur(yellow_threshed,71)	
	#cv2.imwrite(filedir+'yellow_edges.jpg',yellow_threshed)

	contours, hierarchy = cv2.findContours(yellow_threshed,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	yellows = np.zeros(noCols*2+2,dtype = float)
	line = np.zeros(noCols+1,dtype = float)
	#region = 0
	i = 0
	for cnt in contours:
		if cv2.contourArea(cnt)> 1000 and i<noCols*2+2:
			#print cv2.contourArea(cnt)
			M = cv2.moments(cnt)
			col,row = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
			yellows[i] = col
			i = i+1
	
	yellows.sort()

	for cnt in range (0,noCols+1):
		line[cnt] = (yellows[cnt*2:cnt*2+2:]).mean()
	#line[0] = (yellows[0:2:]).mean()
	#line[1] = (yellows[2:4:]).mean()
	#line[2] = (yellows[4:6:]).mean()
	#line[3] = (yellows[6::]).mean()
	#print line
	return line

#Opencv does not returns vertices in a unique order.
#This function brings about a known order;
#TOP LEFT - TOP RIGHT - BOTTOM RIGHT - BOTTOM LEFT.
def rectify(h):
  h = h.reshape((4,2))
  hnew = np.zeros((4,2),dtype = np.float32)

  add = h.sum(1)
  hnew[0] = h[np.argmin(add)]
  hnew[2] = h[np.argmax(add)]

  diff = np.diff(h,axis = 1)
  hnew[1] = h[np.argmin(diff)]
  hnew[3] = h[np.argmax(diff)]
  return hnew

#This function addresses the skewness of post-its.
#Argument 'skew_im' is an outline of a post-it along the vertices.
def get_square(skew_im, name):

	skew_im_copy = skew_im.copy()
	skew_im_copy = cv2.cvtColor(skew_im_copy,cv2.COLOR_BGR2HSV)	
	warp = cv2.resize(skew_im,(450,450))

	if name == 'blue':
		BLUE_MIN = np.array([75, 50, 60],np.uint8)
		BLUE_MAX = np.array([130, 255, 255],np.uint8)
		threshed = cv2.inRange(skew_im_copy, BLUE_MIN, BLUE_MAX)

	if name =='purpink':
		PINK_MIN = np.array([130, 80, 50],np.uint8)
		PINK_MAX = np.array([180, 255, 255],np.uint8)
		threshed = cv2.inRange(skew_im_copy , PINK_MIN, PINK_MAX)

	if name == 'green':
		GREEN_MIN = np.array([35, 100, 60],np.uint8)
		GREEN_MAX = np.array([80, 255, 255],np.uint8)
		threshed = cv2.inRange(skew_im_copy, GREEN_MIN, GREEN_MAX)
	
	#Only one post-it must be detected. Check this from noOfPostIts
	contours, hierarchy = cv2.findContours(threshed,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	
	noOfPostIts1 = 0
	for cnt in contours:
		approx1 = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
		#print cv2.contourArea(cnt)
		if len(approx1)==4 and cv2.contourArea(cnt) > 10000:
			cv2.drawContours(threshed,[cnt],0,(255,255,255),2)
			my_approx = rectify(approx1)
			noOfPostIts1 += 1
			h = np.array([ [0,0],[449,0],[449,449],[0,449] ],np.float32)
			retval = cv2.getPerspectiveTransform(my_approx,h)
			warp = cv2.warpPerspective(skew_im,retval,(450,450))
	if noOfPostIts1 != 1:
		print 'CHECK DUDE. ' + name	

	return warp


#Find post-Its and save them.
def square_contours(threshed_image,original,name,region,label):

	contours, hierarchy = cv2.findContours(threshed_image,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	noOfPostIts = 0
	reg = 0
	for cnt in contours:
		approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
		if len(approx)==4 and cv2.contourArea(cnt) > 10000:
			#print cv2.contourArea(cnt)
			cv2.drawContours(threshed_image,[cnt],0,(255,255,255),2)
			square = approx
			square = rectify(square)
			min_row = square[::,1::].min()
			max_row = square[::,1::].max()
			min_col = square[::,0:1:].min()
			max_col = square[::,0:1:].max()

			skew = original[min_row:max_row:, min_col:max_col: , ::]
			noOfPostIts += 1
			temp_post = get_square(skew,name)
			
			xloc = int((max_col+min_col)/2)
			yloc = int((max_row+min_row)/2)
			
##			if(xloc>region[0] and xloc<region[1]):
##				reg = 1
##			elif(xloc>region[1] and xloc<region[2]):
##				reg = 2
##			elif(xloc>region[2] and xloc<region[3]):
##				reg = 3
			#print reg
				
			for cnt in range(0, noCols):
				if(xloc>region[cnt] and xloc<region[cnt+1]):
					reg = cnt+1
			
			sign = grid_signature(binarize(temp_post))
			#print signature

			post_name = filedir+'post' + str(noOfPostIts+label) + '.jpg'
			txt_name = filedir+'post' + str(noOfPostIts+label) + '.json'
		
			j=json.dumps({'label':noOfPostIts+label,'signature':sign.tolist() , 'x':xloc, 'y':yloc, 'column':reg, 'issueID':filedir[2:]+'post' + str(noOfPostIts+label)+ '.jpg', 'type':name},indent=4)
			f=open(txt_name,'w')
			f.write(j)
			f.close()

			#Save signature and post_it in the working directory.
			#np.savetxt(txt_name,sign,'%10.8f')			
			cv2.imwrite(post_name,temp_post)

	return threshed_image,noOfPostIts


def blue_blobs(hsv_img,original,region):
	
	#Color blobbing for blue in opencv hsv format.
	BLUE_MIN = np.array([75, 75, 60],np.uint8)
	BLUE_MAX = np.array([135, 255, 255],np.uint8)
	blue_threshed = cv2.inRange(hsv_img, BLUE_MIN, BLUE_MAX)
	#Noise removal
	#blue_threshed = cv2.GaussianBlur(blue_threshed,(5,5),5)
	blue_threshed = cv2.medianBlur(blue_threshed,19)
	#blue_threshed = cv2.GaussianBlur(blue_threshed,(5,5),1)
	#cv2.imwrite(filedir+'blue.jpg',blue_threshed)
	b_name = 'blue'
	b_threshed,blues = square_contours(blue_threshed , original , b_name,region,label = 0)
	#cv2.imwrite(filedir+'blue_contours.jpg',b_threshed)
	print str(blues) + ' blues found'
	return blues

def pink_blobs(hsv_img,original,region,label):
	
	#Color blobbing for pink and purple in opencv hsv format.
	PINK_MIN = np.array([130, 90, 50],np.uint8)
	PINK_MAX = np.array([180, 255, 255],np.uint8)
	pur_pink_threshed = cv2.inRange(hsv_img	, PINK_MIN, PINK_MAX)
	#Noise removal 
	pur_pink_threshed = cv2.medianBlur(pur_pink_threshed,21)
	#cv2.imwrite(filedir+'purpink.jpg',pur_pink_threshed)
	p_name = 'purpink'
	p_threshed,purpinks = square_contours(pur_pink_threshed , original, p_name,region,label)
	#cv2.imwrite(filedir+'purpink_contours.jpg',p_threshed)
	print str(purpinks)+' purpinks found' 
	return purpinks

def green_blobs(hsv_img,original,region,label):
	
	#Color blobbing for green in opencv hsv format.
	GREEN_MIN = np.array([35, 80, 60],np.uint8)
	GREEN_MAX = np.array([80, 255, 255],np.uint8)
	green_threshed = cv2.inRange(hsv_img, GREEN_MIN, GREEN_MAX)
	#Noise removal
	green_threshed = cv2.medianBlur(green_threshed,21)
	#cv2.imwrite(filedir+'green.jpg',green_threshed)
	g_name = 'green'
	g_threshed,greens = square_contours(green_threshed , original, g_name,region,label)
	#cv2.imwrite(filedir+'green_contours.jpg',g_threshed)
	print str(greens)+' greens found'
	return greens

def blob(img):

	img = rotateYellows(img)
	cv2.imwrite(filedir+'rotatedOriginal.jpg',img)
	region = column(img)
	original = img.copy()
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)	
	blue_posts = blue_blobs(hsv,img,region)
	purpink_posts = pink_blobs(hsv,img,region,blue_posts)
	green_posts = green_blobs(hsv,img,region,blue_posts+purpink_posts)

	posts=json.dumps({'blues':blue_posts, 'purpinks':purpink_posts, 'greens':green_posts},indent = 4)
	f=open(filedir+'noOfPosts.json','w')
	f.write(posts)
	f.close()

def crop ():
    
  #Read image from which post-its will be cropped.
  im_2_crop = cv2.imread(filedir+'pic.jpg')
  #im_2_crop = cv2.imread('dog_ear.jpg')
  #im_2_crop = cv2.resize(im_2_crop, (2000,2000))
  img = blob(im_2_crop)

print 'starting crop'
crop()
print 'ending crop'
