import serial
from cam import shoot, editImage, tweet
from useRRD import addData, graphRRD

port = serial.Serial('/dev/ttyAMA0',115200,timeout = 1)
data = []

while True:
	dataReceivedString = port.readline()
	currentData = dataReceivedString.split(' ')
	#data.append(currentData)
	print(currentData)
	if currentData != ['']:
		temp = currentData[0]
		lux = currentData[1]
		data.append(currentData)
		if currentData[2] == '1':
			print('shoot!')
			shoot(temp,lux)		
			editImage(temp)
			tweet(temp,lux)
			addData(temp, lux)
			graphRRD()
			print('Tweeted successfully!')
			
