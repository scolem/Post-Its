"""
Copyright 2014 Scott Lemmer, Nelson Ako

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

#This code analysis the similarity between Post-Its 
#taken under different lighting conditions.


import cv2
import numpy as np

const_step = 40 #im_size/5

#Returns the number of dark/black pixels in each 5X5 grid
#The two commented lines can replace the actual code,to enhance speed
#since for loops take time. 
def blackCount(im):
	row, col = im.shape[:2]	
	return row*col - cv2.countNonZero(im)

#Return normalized version of signatures(between 0 and 1)	
def normalize_signature(sign):
	return (sign-sign.min()) / (sign.max() - sign.min())

#5X5 grid of 400X400 image. Returns the image signature(1D array with 28 elements(25+3))
#Image shape must be square and dimensions must be a multiple of 5
def grid_signature(im):
	im_sign = np.zeros(64)
	for i in range(8):
		for j in range(8):
			im_temp = im[i*const_step:i*const_step + const_step:1 , j*const_step:j*const_step + const_step:1]	# 5X5 grid extract
			im_sign[i*8 + j] = blackCount(im_temp)
	im_sign = normalize_signature(im_sign)	
	#im_sign = im_sign*100	
	return im_sign		


#Gets the signatures and checks for similarity
#Returns True for similar and False otherwise.
def compare(sign1,sign2):
#	print sign1
	#print '\n\n'
#	print sign2
	diff = abs(sign1-sign2)
	#tolerance is the number of values greater than 0.4 in array diff.
	tolerance = diff[(diff > 0.3)].size
#	print tolerance
#	print diff
	if tolerance > 5 and diff.max()>0.64:
		#print ' not similar '
		return False
	else:
		#print ' similar '			
		return True

#Reads and converts a color image to grayscale, then to black and white. 
#Also resizes the image. We process 400X400 square images.
def image_preprocessing(imageFilename):
	image = cv2.imread(imageFilename)
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	#Conversion to black and white.
	(thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	im_bw = cv2.resize(im_bw,(320,320))
	return im_bw


def binarize(image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	#Conversion to black and white.
	(thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	im_bw = cv2.resize(im_bw,(320,320))
	return im_bw

#im1 and im2 are examples of some post-its. Try with some other examples as well.
#im1 = image_preprocessing('post9.jpg')
#im2 = image_preprocessing('post7.jpg')
#print compare(grid_signature(im1), grid_signature(im2))
