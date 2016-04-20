import subprocess
#import rrdtool
def createRRD():
	subprocess.call(['rrdtool','create','test.rrd','--step','60',
		'DS:temp:GAUGE:120:-50:50',
		'DS:light:GAUGE:120:0:1000',
		'RRA:MAX:0.5:1:1440' ])

createRRD()
