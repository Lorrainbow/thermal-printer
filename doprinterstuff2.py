#!/usr/bin/python
import random 
import time
import json
import urllib.request
from gpiozero import Button
import board
import busio
import adafruit_thermal_printer

ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)

import serial
uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3000)

printer = ThermalPrinter(uart, auto_warm_up=False)
printer.warm_up()

print_button = Button(12)
poem_button = Button(16)

while True:
	if poem_button.is_pressed:
		print ("poem button")
		
		with urllib.request.urlopen("www.jsonurlgoeshere.com") as url:
			data = json.loads(url.read().decode())
			#print(data)		
			
		randomJob = random.randint(1,len(data["messages"])-1)

		print (data["messages"][randomJob]["job"])
				
		printer.feed(3)					
		printer.size = adafruit_thermal_printer.SIZE_MEDIUM
		printer.bold = True				
 
		printer.print(data["messages"][randomJob]["job"])
		
		printer.bold = False
		printer.size = adafruit_thermal_printer.SIZE_SMALL
		
		printer.feed(5)		
		
		
	if print_button.is_pressed:
		print("print button")		
		
		with urllib.request.urlopen("www.jsonurlgoeshere.com") as url:
			data = json.loads(url.read().decode())
			#print(data)		
			
		category = 0
		
		for i in data["shopping"]:
			if i["category_id"] != category:
				printer.feed(1)
					
				printer.size = adafruit_thermal_printer.SIZE_MEDIUM
				printer.bold = True
				printer.underline = adafruit_thermal_printer.UNDERLINE_THICK

				printer.print(i["category"])
				printer.bold = False
				printer.underline = None				
				printer.size = adafruit_thermal_printer.SIZE_SMALL
		
			printer.print(i["item"])
			category = i["category_id"]            			
		
		printer.feed(3)