import serial
from cam import shoot, editImage, tweet
from useRRD import addData, graphRRD, saveGraphToHtml

port = serial.Serial('/dev/ttyAMA0',115200,timeout = 1)
data = []

while True:
	dataReceivedString = port.readline()
	currentData = dataReceivedString.split(' ')
	print(currentData)
	if len(currentData) == 3:
		temp = currentData[0]
		lux = currentData[1]
		data.append(currentData)
		addData(temp, lux)
                graphRRD()		
		saveGraphToHtml()
		if currentData[2] == '1':
			print('shoot!')
			shoot(temp,lux)		
			editImage(temp)
			tweet(temp,lux)
			print('Tweeted successfully!')	
		
			
