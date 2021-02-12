from PIL import Image
from io import BytesIO
from datetime import datetime
import example
import pgservices

def processImageFromHistoricalData(imgByteArray,filename):

	im = Image.open(BytesIO(imgByteArray))
	
	dateepoch = filename.split("_")
	substring = dateepoch[1].split(".jpg")
	camera = int(substring[0])	
		
	date = datetime.datetime.fromtimestamp(int(dateepoch[0])/1000)

	imageInfo = getImageInfo(im, camera, date)	

	print(imageInfo)
		
	#pgservices.insertCameraData(imageInfo)		
	
def processImageInfoFromLiveData(imgByteArray,camId):
    try:

        im = Image.open(BytesIO(imgByteArray))
        date = datetime.now()
        imageInfo = example.getImageInfo(im, int(camId), date)

        print(imageInfo)

        #pgservices.insertCameraData(imageInfo)

        #TODO Bewerten ob erhöhtes Verkehraufkommen vorliegt
    
