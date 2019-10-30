from ctypes import *
import os
import sys
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import ST7735 as TFT

#pin_meas = 18 	# gpio use board definition
#pin_black = 22	# gpio use board definition
pin_meas = 24 	# gpio use BCM definition
pin_black = 25	# gpio use BCM definition
HOME_DIR = "/home/pi/QSS003_python/"
C12880_LIB = HOME_DIR + "C12880_noLED.so"

spi = SPI.SpiDev(1, 0, max_speed_hz = 4000000)

disp = TFT.ST7735(dc=27, rst = 17, spi = spi, width = 128, height =128)
disp.begin()
disp.clear()

bk = Image.new('RGB', (128,128), (255,255,255))
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",14)
draw = ImageDraw.Draw(bk)
draw.text((10,10),"Hello", font=font, fill =(0,0,0))

disp.display(bk)

time.sleep(1)
C12880 = cdll.LoadLibrary(C12880_LIB)

# board initialization 
C12880.Setup() # init spectrometer
gpio = GPIO.get_platform_gpio()
gpio.setup(pin_meas, GPIO.IN)
gpio.setup(pin_black, GPIO.IN)

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

	# lcd.clear()
	# lcd.cursor_pos = (0, 0)
	# lcd.write_string("Please press")
	# lcd.cursor_pos = (1, 0)
	# lcd.write_string("the button")

	while (1):
		#wait until black or meas buttom is pressed
		while (meas and black):
			if gpio.input(pin_meas) == GPIO.LOW:
				meas = 0
				print("meas low")
			if gpio.input(pin_black) == GPIO.LOW:
				black = 0
				print("black low")

		# lcd.clear()
		# lcd.cursor_pos = (0, 0)
		# lcd.write_string("Measuring....")

		# C12880.LED_Set_Current(1, led1_current)
		# C12880.LED_Set_Current(2, led2_current)
		# C12880.LED_Set_Current(3, led3_current)

		time.sleep(led_stable_time)

		if (black == 0):
			fname = "black.txt"
		else:
			fname = "desktop_" + str(fnameindex) + ".txt"
		fname = HOME_DIR + fname

		C12880.ReadSpectrometer(int_time, data)

		out = [str(line) + '\n' for line in data]
		fp = open(fname, "w+")
		#print(out)
		fp.writelines(out)
		fp.close()

		#lcd.clear()
		# lcd.cursor_pos = (1, 0)
		# lcd.write_string("Writing finish")

		if (meas == 0):
			fnameindex = fnameindex + 1

		# C12880.LED_Set_Current(1, 0) # set LED driver1 current to 0 mA
		# C12880.LED_Set_Current(2, 0) # set LED driver2 current to 0 mA
		# C12880.LED_Set_Current(3, 0) # set LED driver3 current to 0 mA

		meas = 1
		black = 1
		#loop = loop + 1
		print("done")
