import cv2
import cvlib as cv
import numpy as np
from cvlib.object_detection import draw_bbox
import os
import datetime
from PIL import Image

def getImageInfo(im, camera, date):
	if camera == 1:
		leftside = (0, 0, 155, 288)
		rightside = (140, 0, 352, 288)
	elif camera == 2:
		leftside = (0, 0, 380, 576)
		rightside = (380, 0, 720, 576)
	elif camera == 3:
		leftside = (0, 0, 185, 288)
		rightside = (185, 0, 352, 288)
	elif camera == 4:
		leftside = (0, 0, 166, 288)
		rightside = (166, 0, 352, 288)
	elif camera == 5:
		leftside = (0, 0, 350, 576)
		rightside = (350, 0, 720, 576)

	leftImage = im.crop(leftside)
	rightImage = im.crop(rightside)

	vehiclesLeftSide = vehicleDetection(leftImage)
	vehiclesRightSide = vehicleDetection(rightImage)


	infoPerImage = {'camera':camera, 'leftvehicles':vehiclesLeftSide, 'rightvehicles':vehiclesRightSide, 'timestamp':date}
	
	return infoPerImage

def vehicleDetection(image):
	pImage = image.convert('RGB')

	oImage = np.array(pImage)
	oImage = oImage[:, :, ::-1].copy()

	bbox1, label1, conf1 = cv.detect_common_objects(oImage)

	return int(label1.count('car'))+int(label1.count('truck'))
