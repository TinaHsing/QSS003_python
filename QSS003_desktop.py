from ctypes import *
import os
import sys
import time
import smbus2
import subprocess
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

pin_meas = 18 	# gpio use board definition
pin_black = 22	# gpio use board definition
HOME_DIR = "/home/pi/QSS003_python/"
C12880_LIB = HOME_DIR + "C12880.so"

sys.modules['smbus'] = smbus2
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)

C12880 = cdll.LoadLibrary(C12880_LIB)

# board initialization 
C12880.Setup() # init spectrometer
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_black, GPIO.IN)
GPIO.setup(pin_meas, GPIO.IN)
ip = subprocess.check_output(["hostname","-I"])
ip = str(ip)
#print(ip)
ip = ip[2:-4]
#print(ip)
lcd.clear()
lcd.cursor_pos = (0, 0)
lcd.write_string(ip)
#time.sleep(1)

data = (c_uint * 288)() # data to store spectrum data
meas = 1
black = 1
fnameindex = 0
#loop = 0

if len(sys.argv) < 6:
	error_str = str(sys.argv[0]) + " led1_current led2_current led3_current led_stable_time int_time"
	print(error_str)
else:
	led1_current = int(sys.argv[1])
	led2_current = int(sys.argv[2])
	led3_current = int(sys.argv[3])
	led_stable_time = float(sys.argv[4])
	int_time = int(sys.argv[5])

	while (1):
		#wait until black or meas buttom is pressed
		while (meas and black):
			if GPIO.input(pin_meas) == GPIO.LOW:
				meas = 0
				print("meas low")
			if GPIO.input(pin_black) == GPIO.LOW:
				black = 0
				print("black low")

		lcd.clear()
		lcd.cursor_pos = (0, 0)
		lcd.write_string("Measuring....")

		# change LED setting in command line
		C12880.LED_Set_Current(1, led1_current) # set LED driver1 current to setting mA
		C12880.LED_Set_Current(2, led2_current) # set LED driver2 current to setting mA
		C12880.LED_Set_Current(3, led3_current) # set LED driver3 current to setting mA

		# change LED delay time in command line
		time.sleep(led_stable_time)

		if (black == 0):
			fname = "black.txt"
		else:
			fname = "desktop_" + str(fnameindex) + ".txt"
		fname = HOME_DIR + fname

		# change C12880 int time in command line
		C12880.ReadSpectrometer(int_time, data)

		out = [str(line) + '\n' for line in data]
		fp = open(fname, "w+")
		#print(out)
		fp.writelines(out)
		fp.close()

		#lcd.clear()
		lcd.cursor_pos = (1, 0)
		lcd.write_string("Writing finish")

		if (meas == 0):
			fnameindex = fnameindex + 1

		C12880.LED_Set_Current(1, 0) # set LED driver1 current to 0 mA
		C12880.LED_Set_Current(2, 0) # set LED driver2 current to 0 mA
		C12880.LED_Set_Current(3, 0) # set LED driver3 current to 0 mA

		meas = 1
		black = 1
		#loop = loop + 1
		print("done")