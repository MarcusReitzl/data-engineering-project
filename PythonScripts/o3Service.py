import json
import requests

def getO3Url():
	try:
		f = open("/home/de/Project/sources.json")
		data = json.load(f)

		for trafficinfo in data["trafficInfo"]:
			if trafficinfo["channelID"] == "O3":
				return trafficinfo["url"]
		return None
		f.close()
	except Exception as e:
		print(e)

def loadJsonFromUrl(url):
	try:
		response = requests.get(url)
		data = response.json()

		return data
	except Exception as e:
		print(e)

def getAdditionalTrafficInformation(camInfo):	
	try:
		url = getO3Url()
		if url is None:
			return None
		
		json = loadJsonFromUrl(url)

		for item in json["TrafficItems"]:
			if item["Street"] == camInfo:
				return item["Text"]
		return None
	except Exception as e:
		print(e)
def printAdditionalTrafficInformation(camInfo):
	trafficInfo = getAdditionalTrafficInformation(camInfo)
	try:			
		if trafficInfo is not None:
			print(trafficInfo)
		else:
			print("no additional TrafficInformation")
	except Exception as e:
		print(e)
	
#printAdditionalTrafficInformation("A2")



