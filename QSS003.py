from ctypes import *
import os
import time
import subprocess
import RPi.GPIO as GPIO

pin_meas = 18 	# gpio use board definition
pin_black = 22	# gpio use board definition
SETTING_FILENAME = "setting.txt"

C12880 = cdll.LoadLibrary('/home/pi/QSS003_python//C12880.so')

# board initialization 
C12880.Setup() # init spectrometer
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_black, GPIO.IN)
GPIO.setup(pin_meas, GPIO.IN)
ip = subprocess.check_output(["hostname","-I"])
#print(ip)
ip = str(ip)
ip = ip[0:-2]
#print(ip)
C12880.LCD_Clear()
C12880.LCD_Write(0, 0, ip)

data = (c_uint * 288)() # data to store spectrum data


#open file for parameter setting
param = [0, 0, 0, 0, 0]
if os.path.exists(SETTING_FILENAME):
   param = [line.rstrip('\n') for line in open(SETTING_FILENAME)]
#print param

led1_current = int(param[0])
led2_current = int(param[1])
led3_current = int(param[2])
led_stable_time = float(param[3])
int_time = int(param[4])

#wait until black or meas buttom is pressed
measb = 1
fnameindex = 0
black = 0
loop = 1
while loop:
	#while (measb):
	#	if GPIO.input(pin_meas) == GPIO.HIGH:
	#		measb = 0
	#	if GPIO.input(pin_black) == GPIO.HIGH:
	#		measb = 0
	#		black = 1

	#C12880.LCD_Clear()
	C12880.LCD_Write(0, 1, b"Measuring....")

	C12880.LED_Set_Current(1, 25) # set LED driver1 current to 25mA
	C12880.LED_Set_Current(2, 15) # set LED driver2 current to 15mA
	C12880.LED_Set_Current(3, 5) # set LED driver3 current to 5mA

	time.sleep(led_stable_time)

	if (black):
		fname = "black.txt"
	else:
		fname = str(fnameindex) + ".txt"

	C12880.ReadSpectrometer(int_time, data)

	out = [str(line) + '\n' for line in data] 
	fp = open(fname, "w+")
	fp.writelines(out)
	fp.close()

	C12880.LCD_Clear()
	C12880.LCD_Write(0, 0, b"Writing finish")

	if (black == 0):
		fnameindex = fnameindex + 1

	measb = 1
	black = 0
	loop = 0	#remark this line will loop always
	print("done")
