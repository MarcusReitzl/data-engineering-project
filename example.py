import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import numpy as np
from cvlib.object_detection import draw_bbox
import os
import datetime
from PIL import Image
import psycopg2
import pgservices

def getImageInfo(im, camera, date):
#TODO ins Json-File speichern, damit if else block wegfällt
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

def processImagesFromDirectory(directory):

	imageInfoList = []

	for filename in os.listdir(directory):
		if filename.endswith(".jpg"):
			dateepoch = filename.split("_")
			substring = dateepoch[1].split(".jpg")
			camera = int(substring[0])
			#date = datetime.datetime.fromtimestamp(int(dateepoch[0])/1000).strftime('%Y-%m-%d %H:%M:%S')
			date = datetime.datetime.fromtimestamp(int(dateepoch[0])/1000)
			name = directory + filename
			file=name
			#im = cv2.imread(file)
			try:
				im = Image.open(file)
			except Exception as e:
	    			print("Uh oh, crappy image skipped")
	    			print(e)
	    			continue
			

			
			imageInfo = getImageInfo(im, camera, date)
			print(imageInfo)
			imageInfoList.append(imageInfo)
		else:
			continue

	return imageInfoList
	

def insertDB():
	for dict in sorted(infoImages, key = lambda i: i['camera']):
		pgservices.insertCameraData(dict)

def calcAverage(infoImages):
	averages = []
	for dict in sorted(infoImages, key = lambda i: i['timestamp']): 
		print(dict['timestamp'])
		weekday = dict['timestamp'].weekday();
		hour = dict['timestamp'].hour
		print(weekday)
		print(hour)
		
		
def main():
	##pgservices.dropTables()
	#pgservices.createTableInfo()
	pgservices.selectTable()
	#pgservices.selectTime()

	#infoImages = processImagesFromDirectory("/home/de/testspark/camPictures/")

	#calcAverage(infoImages)
	##pgservices.insertCameraDatafromList(infoImages)
	#pgservices.createTableAverage()
	##pgservices.insertAverageData()
	##pgservices.selectAverageData()
	


if __name__ == "__main__":
    main()
