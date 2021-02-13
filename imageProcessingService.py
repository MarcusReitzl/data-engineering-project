#!/usr/bin/python

import sys
from PIL import Image
from io import BytesIO
import datetime
import example
import pgservices
import base64

def processImageFromHistoricalData(imgByteArray,filename):
	
	image = base64.b64decode(imgByteArray)  
	im = Image.open(BytesIO(image))
	
	dateepoch = filename.split("_")
	substring = dateepoch[1].split(".jpg")
	camera = int(substring[0])	
		
	date = datetime.datetime.fromtimestamp(int(dateepoch[0])/1000)

	imageInfo = example.getImageInfo(im, camera, date)	

	print(imageInfo)
		
	pgservices.insertCameraData(imageInfo)		
	
def processImageInfoFromLiveData(imgByteArray,camId):

        im = Image.open(BytesIO(imgByteArray))
        date = datetime.now()
        imageInfo = example.getImageInfo(im, int(camId), date)

        print(imageInfo)

        pgservices.insertCameraData(imageInfo)

        #TODO Bewerten ob erhoehtes Verkehraufkommen vorliegt
        
        
def main():
	#print("test")
	#print("Key: "+sys.argv[1]+" Value: "+ sys.argv[2])
	print(sys.argv[2])
	processImageFromHistoricalData(sys.argv[1],sys.argv[2])
	
	
	

if __name__ == "__main__":
	main()
	
