#import rrdtool
import subprocess
from PIL import Image

def addData(temperature,light):
	subprocess.call([ 'rrdtool','update','test.rrd',
				'N' + ':' + 
				str(temperature) + ':' + 
				str(light) ])
	print('data update')
def graphRRD():
	subprocess.call([ 'rrdtool','graph','test.png',
			'-w','1000','-h','400',
			'--start', str(-36000),
			'--end', 'now',
			'DEF:temperature=test.rrd:temp:MAX',
			'DEF:light=test.rrd:light:MAX',
			'LINE1:temperature#ff0000:Temp',
			'LINE2:light#00ff00:Light' ])
	print('graph updated')

def saveGraphToHtml():
	graph = Image.open('test.png')
	graph.save('/var/www/html/graph.png')
