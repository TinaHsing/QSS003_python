from ctypes import *
import os
import sys
import time
import datetime
import subprocess
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import ST7735 as TFT
import pigpio


pin_meas = 24 	# gpio use bcm definition
pin_black = 25	# gpio use bcm definition

HOME_DIR = "/home/pi/QSS003_python/"
C12880_LIB = HOME_DIR + "Dual_C12880.so"

GATE_LED_PIN1 = 4	# 7 in BOARD
GATE_LED_PIN2 = 22	# 15 in BOARD
PWM_LED_PIN1 = 18 # in pigpio
PWM_LED_PIN2 = 13 # in pigpio

PWM_FREQ = 500
DUTY_MIN = 0
DUTY_MAX = 900000	# original = 1000000
LED_CURR_MIN = 60	#mA
LED_CURR_MAX = 330	#mA
LED_DUTY_CONST = 100000/3

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

LINE1Y = 15
LINE2Y = 30
LINE3Y = 45
LINE4Y = 65
LINE5Y = 80
LINE6Y = 100

SPACE1 = 15
SPACE2 = 20

time.sleep(1)
C12880 = cdll.LoadLibrary(C12880_LIB)

if len(sys.argv) < 6:
	error_str = str(sys.argv[0]) + " led1_current led2_current led_stable_time int_time1 int_time2"
	print(error_str)
else:
	# board initialization 
	C12880.Setup() # init spectrometer
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(pin_meas, GPIO.IN)
	GPIO.setup(pin_black, GPIO.IN)
	GPIO.setup(GATE_LED_PIN1, GPIO.OUT)
	GPIO.setup(GATE_LED_PIN2, GPIO.OUT)
	GPIO.output(GATE_LED_PIN1, GPIO.HIGH)	#close
	GPIO.output(GATE_LED_PIN2, GPIO.HIGH)	#close

	data1 = (c_uint * 288)() # data to store spectrum data
	data2 = (c_uint * 288)()
	meas = 1
	black = 1
	fnameindex = 0

	# Display init
	spi = SPI.SpiDev(SPI_PORT, SPI_CH, max_speed_hz = SPI_SPEED)
	disp = TFT.ST7735(dc = AOPIN, rst = RSTPIN, spi = spi, width = 128, height = 128)
	disp.begin()
	disp.clear()		
	img = Image.new('RGB', TFT_SIZE, COLOR_WHITE)
	draw = ImageDraw.Draw(img)
	font = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
	fontout = ImageFont.truetype(font,11)
	draw.text((0,LINE1Y), "    Mode: Measure", font = fontout, fill = COLOR_BLUE)
	draw.text((0,LINE2Y), "  Bilirubin", font = fontout, fill = COLOR_BLUE)
	draw.text((0,LINE4Y), "  SiO2", font = fontout, fill = COLOR_BLUE)
	disp.display(img)

	led1_current = int(sys.argv[1])
	led2_current = int(sys.argv[2])
	led_stable_time = float(sys.argv[3])
	int_time1 = int(sys.argv[4])
	int_time2 = int(sys.argv[5])

	if (led1_current < LED_CURR_MIN):
		led1_current = LED_CURR_MIN
	elif (led1_current > LED_CURR_MAX):
		led1_current = LED_CURR_MAX

	if (led2_current < LED_CURR_MIN):
		led2_current = LED_CURR_MIN
	elif (led2_current > LED_CURR_MAX):
		led2_current = LED_CURR_MAX

	print("led1_current = "+ str(led1_current))
	print("led2_current = "+ str(led2_current))

	led1_duty = (led1_current - LED_CURR_MIN)*LED_DUTY_CONST
	led2_duty = (led2_current - LED_CURR_MIN)*LED_DUTY_CONST

	print("led1_duty = "+ str(led1_duty))
	print("led2_duty = "+ str(led2_duty))

	pi = pigpio.pi()
	pi.hardware_PWM(PWM_LED_PIN1, PWM_FREQ, int(led1_duty))
	pi.hardware_PWM(PWM_LED_PIN2, PWM_FREQ, int(led2_duty))

	while (0):
		#wait until black or meas buttom is pressed
		while (meas and black):
			if GPIO.input(pin_meas) == GPIO.LOW:
				meas = 0
				print("meas low")
			if GPIO.input(pin_black) == GPIO.LOW:
				black = 0
				print("black low")

		if (led1_duty > 0):
			GPIO.output(GATE_LED_PIN1, GPIO.LOW)	# open
		if (led2_duty > 0):
			GPIO.output(GATE_LED_PIN2, GPIO.LOW)	# open

		time.sleep(led_stable_time)

		if (black == 0):
			fname = "black.txt"
		else:
			fname = "desktop_" + str(fnameindex) + ".txt"
		fname = HOME_DIR + fname

		#C12880.ReadSpectrometer(int_time, data)
		C12880.Read2Spectrometer(int_time1, int_time2, data1, data2)

		# print the data on tft screen 
		draw.rectangle((0, LINE3Y, 128, LINE3Y+SPACE2), COLOR_WHITE)
		draw.rectangle((0, LINE5Y, 128, LINE5Y+SPACE2), COLOR_WHITE)
		draw.rectangle((0, LINE6Y, 128, LINE6Y+SPACE1), COLOR_WHITE)
		fontout = ImageFont.truetype(font,16)
		draw.text((0,LINE3Y),"  12.1 mg/dL", font = fontout, fill = COLOR_RED)
		draw.text((0,LINE5Y),"     66%", font = fontout, fill = COLOR_RED)
		fontout = ImageFont.truetype(font,10)
		draw.text((0,LINE6Y),str(datetime.datetime.now()), font = fontout, fill = COLOR_BLUE)
		disp.display(img)

		# out = [str(line) + '\n' for line in data]
		# fp = open(fname, "w+")
		# #print(out)
		# fp.writelines(out)
		# fp.close()

		if (meas == 0):
			fnameindex = fnameindex + 1

		pi.hardware_PWM(PWM_LED_PIN1, PWM_FREQ, 0)
		pi.hardware_PWM(PWM_LED_PIN2, PWM_FREQ, 0)
		GPIO.output(GATE_LED_PIN1, GPIO.HIGH) # close
		GPIO.output(GATE_LED_PIN2, GPIO.HIGH) # close

		meas = 1
		black = 1

		print("done")
