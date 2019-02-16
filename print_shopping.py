#!/usr/bin/python

import time
import json
import glob
import os
from gpiozero import Button
from Adafruit_Thermal import *

button = Button(12)
printer = Adafruit_Thermal("/dev/ttyUSB0", 9600, timeout=5)

while True:
	if button.is_pressed:		
		#any new json files? 
		new_files = sorted(glob.glob('/home/pi/jsonin/*'))
		if new_files:
			#open and reload the data
			with open('/home/pi/jsonin/alldata.json') as json_data:
				d = json.load(json_data)

			#os.remove(new_files[0])
				
			shopping_list = []
			
			f = open("/dev/ttyUSB0", "w")
			category = 0
			
			for i in d["shopping"]:
				if i["category_id"] != category:
					printer.feed(1)
					printer.setSize('M')
					printer.boldOn()
					printer.underlineOn()
					printer.println(i["category"])
					printer.boldOff()
					printer.underlineOff()
					printer.setSize('S')
				
				printer.println(i["item"])
				category = i["category_id"]            
				shopping_list.append(i["item"])
				
			f.write ("\n\n\n")
			f.close()			
			
