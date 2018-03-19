#!/usr/bin/env python

from time import sleep # to add delays

import string
import time
import os
from time import gmtime, strftime

VIRTUAL_SENSOR_NAME = 'virtualSensorFolder'

flagStatus = 0

def updateVirtualSensorValue( data ):
	global status
	data = str(data).strip()		
	print str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) + "  Update VS - value: " + str(data)

	dataIot = open(directory + file, "w")
	dataIot.write(str(flagStatus) + ',' + data)
	dataIot.flush()
	dataIot.close()
	if flagStatus == 0 :
		flagStatus = 1
	elif flagStatus == 1:
		flagStatus = 0


def checkOutputFolder():
	file = 'data'
	directory = '/sensors/'+ VIRTUAL_SENSOR_NAME +'/'
	print 'Checking directory exists ...'
	if not os.path.exists(directory):
		print 'Directory does not exists... creating... '
		try:
			os.makedirs(directory)
			print 'OK'
		except OSError as e:
			print 'NO \n ERROR:' + e
			exit()
	else:
		print 'OK'


daf main():
	checkOutputFolder()
	
	while True: # Run forever
		keyboardInput = raw_input()
		
		## parse string to int
		
		updateVirtualSensorValue( keyboardInput )	
		sleep(0.1) # wait a second
    
    
if __name__ == "__main__":
	main()
