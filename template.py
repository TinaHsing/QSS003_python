from ctypes import *
import math

Quantaser = cdll.LoadLibrary("filepath/Quantaser.so") # so data provided by Quantaser
#read prameter setting from file
#user need to write their setting into setting.txt throgh ssh before use
file fp = open("setting.txt")
fp.close()
param = [line.rstrip("\n") for line in fp]
ledcurrent =param[0:5]
c12880time = param[6]
index =0
repeat = param[7]
while True:
	mode = Quantaser.readGPIOstatsu()
	Quantaser.setLEDCurrent(ledcurrent)
	#wait until measurement button is pressed
	while gpio_some_pin ==0:
	#turn on measurement led indicator
	
	if mode == 1: # Portable mode
		###### You can addsome code to calculate bilirubin
		Quantaser.turnon_MeasurementLED()
		#start measurement
		spectro = Quantaser.measure(c12880time)
		#turn off measurement led indicator
		Quantaser.turnoff_MeasurementLED()
		bilirubin = math.sqrt(sum(spectro))
		Quantaser.data_to_lcd(row=0,col=0,str(bilirubin)+"   "+str(index)) # write data with index info to lcd row=0, col=0
	if mode == 2: # Laptop mode		
		for i in range(repeat):
			###### You can addsome code to calculate bilirubin
			Quantaser.turnon_MeasurementLED()
			#start measurement
			spectro = Quantaser.measure(c12880time)
			#turn off measurement led indicator
			Quantaser.turnoff_MeasurementLED()
			#save file with target file name
			fp =open("targetfilename with index")
			Quantaser.data_to_lcd(row =0, col=0,"filename index") 
			fp.write(spoectro)
			fp.close()
		#user can read the spoectro data by ssh  
	if mode ==3: # nonskin mode	
		Quantaser.turnon_MeasurementLED()
		#start measurement
		spectro = Quantaser.measure(c12880time)
		#turn off measurement led indicator
		Quantaser.turnoff_MeasurementLED()
		#save file with target file name
		fp =open("nonskin file name")
		fp.write(spoectro)
		fp.close()
		Quantaser.data_to_lcd(row =0, col=0,"nonskin file name mode") 	

	index = index+1




