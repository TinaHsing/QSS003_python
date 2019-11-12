from ctypes import *
import os
import sys
import time
import RPi.GPIO as GPIO


pin_meas = 18 	# gpio use board definition
pin_black = 22	# gpio use board definition
HOME_DIR = "/home/pi/QSS003_python/"
C12880_LIB = HOME_DIR + "C12880.so"

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

time.sleep(1)
C12880 = cdll.LoadLibrary(C12880_LIB)

# board initialization 
C12880.Setup() # init spectrometer
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_meas, GPIO.IN)
GPIO.setup(pin_black, GPIO.IN)

data = (c_uint * 288)() # data to store spectrum data
meas = 1
black = 1
fnameindex = 0

# Display init

spi = SPI.SpiDev(SPI_PORT, SPI_CH, max_speed_hz = SPI_SPEED)
disp = TFT.ST7735(dc=AOPIN, rst = RSTPIN, spi = self.spi, width = TFT_WIDTH, height = TFT_HEIGHT)
disp.begin()
disp.clear()		
img = Image.new('RGB', TFT_SIZE, COLOR_WHITE)
draw = ImageDraw.Draw(self.img)
font = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
fontout = ImageFont.truetype(font,10)
draw.text((0,10),"  Measure",font = fontout, fill = COLOR_BLUE)
draw.text((0,20), "Bilirubin", font = fontout, fill = COLOR_BLUE)
draw.text((0,40), "SiO2", font = fontout, fill = COLOR_BLUE)
disp.display(img)
		

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

		# lcd.cursor_pos = (0, 0)
		# lcd.write_string("Measuring....")

		C12880.LED_Set_Current(1, led1_current)
		C12880.LED_Set_Current(2, led2_current)
		C12880.LED_Set_Current(3, led3_current)

		time.sleep(led_stable_time)

		if (black == 0):
			fname = "black.txt"
		else:
			fname = "desktop_" + str(fnameindex) + ".txt"
		fname = HOME_DIR + fname

		C12880.ReadSpectrometer(int_time, data)

		# print the data on tft screen 
		draw.rectangle(0,30,128,50, COLOR_WHITE)
		draw.rectangle(0, 50, 128, 70, COLOR_WHITE)
		draw.rectangle(0, 70, 128, 80, COLOR_WHITE)
		fontout = ImageFont.truetype(font,14)
		draw.text((0,30),"12.1 mg/dL",font = fontout, fill = COLOR_RED)
		draw.text((0,50),"66%", font=fontout, fill = COLOR_RED)
		fontout = ImageFont.truetype(font,10)
		draw.text(0,70,str(time.time()),font = fontout, fill = COLOR_BLUE)
		disp.display(img)
		
		out = [str(line) + '\n' for line in data]
		fp = open(fname, "w+")
		#print(out)
		fp.writelines(out)
		fp.close()

		if (meas == 0):
			fnameindex = fnameindex + 1

		C12880.LED_Set_Current(1, 0) # set LED driver1 current to 0 mA
		C12880.LED_Set_Current(2, 0) # set LED driver2 current to 0 mA
		C12880.LED_Set_Current(3, 0) # set LED driver3 current to 0 mA

		meas = 1
		black = 1
		#loop = loop + 1
		print("done")

