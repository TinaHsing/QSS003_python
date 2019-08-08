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
SETTING_FILENAME = HOME_DIR + "setting.txt"
C12880_LIB = HOME_DIR + C12880.so

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
time.sleep(1)

data = (c_uint * 288)() # data to store spectrum data

#open file for parameter setting
param = [0, 0, 0, 0, 0]
if os.path.exists(SETTING_FILENAME):
   param = [line.rstrip('\n') for line in open(SETTING_FILENAME)]
#print(param)

led1_current = int(param[0])
led2_current = int(param[1])
led3_current = int(param[2])
led_stable_time = float(param[3])
int_time = int(param[4])

#wait until black or meas buttom is pressed
measb = 1
fnameindex = 0
black = 0
loop = 0
while (loop < 1):
	#while (measb):
	#	if GPIO.input(pin_meas) == GPIO.HIGH:
	#		measb = 0
	#	if GPIO.input(pin_black) == GPIO.HIGH:
	#		measb = 0
	#		black = 1

	lcd.clear()
	lcd.cursor_pos = (0, 0)
	lcd.write_string("Measuring....")

	C12880.LED_Set_Current(1, led1_current) # set LED driver1 current to 25mA
	C12880.LED_Set_Current(2, led2_current) # set LED driver2 current to 25mA
	C12880.LED_Set_Current(3, led3_current) # set LED driver3 current to 25mA

	time.sleep(led_stable_time)

	if (black):
		fname = "black.txt"
	else:
		fname = str(fnameindex) + ".txt"
	fname = HOME_DIR + fname

	C12880.ReadSpectrometer(int_time, data)

	out = [str(line) + '\n' for line in data] 
	fp = open(fname, "w+")
	fp.writelines(out)
	fp.close()

	#lcd.clear()
	lcd.cursor_pos = (1, 0)
	lcd.write_string("Writing finish")

	if (black == 0):
		fnameindex = fnameindex + 1

	measb = 1
	black = 0
	loop = loop + 1	#remark this line will loop always
	print("done")
