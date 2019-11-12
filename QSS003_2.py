from ctypes import *
import os
#import sys
import time
import subprocess
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import ST7735 as TFT


pin_meas = 24 	# gpio use bcm definition
pin_black = 25	# gpio use bcm definition
pin_dark = 7	# gpio use bcm definition
HOME_DIR = "/home/pi/QSS003_python/"
SETTING_FILENAME = HOME_DIR + "setting.txt"
C12880_LIB = HOME_DIR + "C12880.so"

C12880 = cdll.LoadLibrary(C12880_LIB)

AOPIN = 27
RSTPIN = 17
SPI_PORT = 1
SPI_CH = 0
SPI_SPEED = 4000000
COLOR_RED 	= (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE	= (0,0,255)
COLOR_WHITE	= (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_YELLOW = (255,255,0)
COLOR_PURPLE = (255,0, 255)
COLOR_CYAN = (0, 255,255)
TFT_SIZE = (128, 128)


# board initialization 
C12880.Setup() # init spectrometer
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_meas, GPIO.IN)
GPIO.setup(pin_black, GPIO.IN)
GPIO.setup(pin_dark, GPIO.IN)

data = (c_uint * 288)() # data to store spectrum data
meas = 1
black = 1
dark = 1
fnameindex = 0
#loop = 0
spi = SPI.SpiDev(SPI_PORT, SPI_CH, max_speed_hz = SPI_SPEED)
disp = TFT.ST7735(dc=AOPIN, rst = RSTPIN, spi = spi, width = 128, height = 128)
disp.begin()
disp.clear()		
img = Image.new('RGB', TFT_SIZE, COLOR_WHITE)
draw = ImageDraw.Draw(img)
font = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
fontout = ImageFont.truetype(font,11)
draw.text((0,15),"    Mode: Measure",font = fontout, fill = COLOR_BLUE)
draw.text((0,30), "  Bilirubin", font = fontout, fill = COLOR_BLUE)
draw.text((0,55), "  SiO2", font = fontout, fill = COLOR_BLUE)
disp.display(img)

def ShowIP():
	ip = subprocess.check_output(["hostname","-I"])
	ip = str(ip)
	#print(ip)
	ip = ip[2:-4]
	#print(ip)
	fontout = ImageFont.truetype(font,10)
	draw.rectangle((0,105, 128,115 ), COLOR_WHITE)
	draw.text((0,105), ip, font =fontout, fill = COLOR_BLUE)
	disp.display(img)
#open file for parameter setting
param = [10, 10, 10, 0.01, 1000]
if os.path.exists(SETTING_FILENAME) == False:
	draw.retangle((0,105, 128, 115), COLOR_WHITE)
	draw.text((0,105), "init_err", fontout, fill = COLOR_BLUE)
	disp.display(img)
else:
	param = [line.rstrip('\n') for line in open(SETTING_FILENAME)]
	#print(param)
	led1_current = int(param[0])
	led2_current = int(param[1])
	led3_current = int(param[2])
	led_stable_time = float(param[3])
	int_time = int(param[4])	

	while (1):
		#wait until black or meas buttom is pressed
		while (meas and black and dark):
			if GPIO.input(pin_meas) == GPIO.LOW:
				meas = 0
				
			if GPIO.input(pin_black) == GPIO.LOW:
				black = 0
				
			if GPIO.input(pin_dark) == GPIO.LOW:
				dark = 0
				

		if (dark == 0):
			ShowIP()
			time.sleep(1)
			dark = 1
		else:
			C12880.LED_Set_Current(1, led1_current)
			C12880.LED_Set_Current(2, led2_current)
			C12880.LED_Set_Current(3, led3_current)

			time.sleep(led_stable_time)

			if (black == 0):
				fname = "black.txt"
			else:
				fname = "data_" + str(fnameindex) + ".txt"
			fname = HOME_DIR + fname

			C12880.ReadSpectrometer(int_time, data)

			draw.rectangle((0,55,128,75), COLOR_WHITE)
			draw.rectangle((0, 85, 128, 10), COLOR_WHITE)
			draw.rectangle((0, 70, 128, 80), COLOR_WHITE)
			fontout = ImageFont.truetype(font,14)
			draw.text((0,30),"12.1 mg/dL",font = fontout, fill = COLOR_RED)
			draw.text((0,50),"66%", font=fontout, fill = COLOR_RED)
			fontout = ImageFont.truetype(font,10)
			draw.text((0,105),str(time.time()),font = fontout, fill = COLOR_BLUE)
			disp.display(img)

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
