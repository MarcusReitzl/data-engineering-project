
import sys
from PIL import Image
from io import BytesIO
import datetime
import imageProcessingService
import pgService
import base64

try:
	image = base64.b64decode(sys.argv[1]) 
	filename = sys.argv[2]

	im = Image.open(BytesIO(image))

	dateepoch = filename.split("_")
	substring = dateepoch[1].split(".jpg")
	camera = int(substring[0])	

	date = datetime.datetime.fromtimestamp(int(dateepoch[0])/1000)


	print("start process with " + camera)
	imageInfo = imageProcessingService.getImageInfo(im, camera, date)	
	print("end process")
	print(imageInfo)

	pgService.insertCameraData(imageInfo)		

except Exception as e:
	print(e)

