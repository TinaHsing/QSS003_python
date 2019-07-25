from ctypes import *
import subprocess
import RPi.GPIO as GPIO

pin_meas = 18 	# gpio use board definition
pin_black = 22	# gpio use board definition

C12880 = cdll.LoadLibrary('/home/pi/QSS003_python//C12880.so')

# board initialization 
C12880.Setup() # init spectrometer
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_black, GPIO.INPUT)
GPIO.setup(pin_meas, GPIO.INPUT)
ip = subprocess.check_ouput(["hostname","-I"])
ip = str(ip)
ip = ip(2:-4) #get the ip addresss
C12880.LCD_Clear()
C12880.LCD_Write(0, 0, ip)

data = (c_uint * 288)() # data to store spectrum data


#open file for parameter setting
fp = open("setting.txt")
param = []
i = 0
for line in fp:
	param[i] = line
	i = i + 1
fp.close()

led1_current = param[0]
led2_current = param[1]
led3_current = param[2]
led_stable_time = param[3]
int_time = param[4]

#wait until black or meas buttom is pressed
measb = 1
fnameindex = 0
black = 0
while 1:
	while (measb):
		if GPIO.input(pin_meas) == GPIO.HIGH:
			measb = 0
		if GPIO.input(pin_black) == GPIO.HIGH:
			measb = 0
			black = 1

	C12880.LCD_Clear()
	C12880.LCD_Write(0, 0, "Measuring....")

	C12880.LED_Set_Current(1, 25) # set LED driver1 current to 25mA
	C12880.LED_Set_Current(2, 15) # set LED driver2 current to 15mA
	C12880.LED_Set_Current(3, 5) # set LED driver3 current to 5mA

	sleep(led_stable_time)

	if (black):
		fname = "black.txt"
	else:
		fname = str(fnameindex)+".txt"
	fp = open(fname)
	C12880.ReadSpectrometer(int_time, data)

	for i in range(0,288):
		out = str(data[i])+"\n"
		fname.write(out)
	fp.close()
	C12880.LCD_Clear()
	C12880.LCD_Write(0,0,"333")
	if (black == 0):
		fnameindex=fnameindex+1
	measb = 1
	black = 0
