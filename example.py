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





def cropImage(im, leftside, rightside, camera, date, infoImages):

	s1 = im.crop(leftside)
	s2 = im.crop(rightside)

	ps1 = s1.convert('RGB')
	ps2 = s2.convert('RGB')

	os1 = np.array(ps1)
	os1 = os1[:, :, ::-1].copy() 

	os2 = np.array(ps2)
	os2 =  os2[:, :, ::-1].copy() 



	#lefthalf
	bbox1, label1, conf1 = cv.detect_common_objects(os1)
	#righthalt
	bbox2, label2, conf2 = cv.detect_common_objects(os2)

	#bbox, label, conf = cv.detect_common_objects(im)

	#overrided by each iteration
	infoPerImage = {'camera':camera, 'leftvehicles':int(label1.count('car'))+int(label1.count('truck')), 'rightvehicles':int(label2.count('car'))+int(label2.count('truck')), 'timestamp':date}
	
	infoImages.append(infoPerImage)
	
	#print(dict)

	#output_image = draw_bbox(im, bbox, label, conf)
	#plt.imshow(output_image)
	#plt.show()

	#print(filename+' Number of trucks in the image is '+str(label1.count('truck')))
	#print(filename+' Number of cars in the image is '+ str(label1.count('car'))) 	
	#print(filename+' Number of trucks in the image is '+str(label2.count('truck')))
	#print(filename+' Number of cars in the image is '+ str(label2.count('car'))) 			
	


def getInfoImages(infoImages):
	directory = "/home/de/Project/archive/archive/cams/"
	#directory = "/home/de/Project/Example_Python/"
	

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
			
			if camera == 1:
				leftside = (0,0,155,288)
				rightside = (140,0,352,288)
			elif camera ==2:
				leftside = (0,0,380,576)
				rightside = (380,0,720,576)
			elif camera == 3:
				leftside = (0,0,185,288)
				rightside = (185,0,352,288)
			elif camera == 4:
				leftside = (0,0,166,288)
				rightside = (166,0,352,288)
			elif camera == 5:
				leftside = (0,0,350,576)
				rightside = (350,0,720,576)
			
			cropImage(im, leftside, rightside, camera, date, infoImages)
				
		else:
			continue


#print(InfoImages)		
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
	pgservices.dropTables()
	pgservices.createTableInfo()
	#pgservices.selectTable()
	#pgservices.selectTime()
	infoImages = []
	getInfoImages(infoImages)
	#calcAverage(infoImages)
	pgservices.insertCameraDatafromList(infoImages)
	pgservices.createTableAverage()
	pgservices.insertAverageData()
	pgservices.selectAverageData()
	


if __name__ == "__main__":
    main()
	
 
		
	





