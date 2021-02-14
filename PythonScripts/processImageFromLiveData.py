import sys
from PIL import Image
from io import BytesIO
import datetime
import imageProcessingService
import pgService
import base64
import json
import o3Service




def getCameraDesc(camId):
	f = open("/home/de/Project/sources.json")
	data = json.load(f)

	for cam in data['cams']:
		if cam['camID'] == camId:
			return cam['desc']
	
	return None
	f.close()

try:
	imgByteArray = sys.argv[1]
	camId = sys.argv[2]	
	camDesc = getCameraDesc(camId)
	
	
	image = base64.b64decode(imgByteArray)
	im = Image.open(BytesIO(image))


	date = datetime.datetime.now()

	print("start process with " + camId)
	imageInfo = imageProcessingService.getImageInfo(im, int(camId), date)
	print("end process")
	print(imageInfo)

	pgService.insertCameraData(imageInfo)

	averageInfo = pgService.getAverageInfo(camId,date)

	left = imageInfo["leftvehicles"]
	right = imageInfo["rightvehicles"]

	leftAverage = averageInfo[0]
	rightAverage = averageInfo[1]




	threshold = 1.5

	if left > 0:
		if left >= leftAverage * threshold:
			print("Erhöhtes Verkehrsaufkommen bei Kamera "+ camId + ", " + camDesc + " in entgegenkommender Richtung")
		else:
			print("Niedriges Verkehrsaufkommen bei Kamera "+ camId + ", " + camDesc + " in entgegenkommender Richtung")

	else:
		print("Kein Verkehr bei Kamera "+ camId + ", " + camDesc + " in entgegenkommender Richtung")


	if right > 0:
		if right >= rightAverage * threshold:
			print("Erhöhtes Verkehrsaufkommen bei Kamera "+ camId + ", " + camDesc + " in Fahrtrichtung")
		else:
			print("Niedriges Verkehrsaufkommen bei Kamera "+ camId + ", " + camDesc + " in Fahrtrichtung")	

	else:
		print("Kein Verkehr bei Kamera "+ camId + ", " + camDesc + " in Fahrtrichtung")


	camInfo = camDesc.split(",")
	o3Service.printAdditionalTrafficInformation(camInfo[0])

except Exception as e:
	print(e)

