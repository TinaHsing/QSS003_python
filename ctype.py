import time
from ctypes import *

C12880 = cdll.LoadLibrary('/home/pi/QSS003_python//C12880.so')
C12880.Setup()
time.sleep(1)
data = (c_uint * 288)()
#C12880.ReadSpectrometer(10, data)
#for i in range(0,288):
#	print(data[i])

#C12880.LED_Set_Current(1, 25) # set LED driver1 current to 25mA
#C12880.LED_Set_Current(2, 15) # set LED driver2 current to 15mA
#C12880.LED_Set_Current(3, 5) # set LED driver3 current to 5mA

text =["abcdefg", "ABCDEFG"]
for i in range(10)
	j=i%2
	C12880.LCD_Clear()
	C12880.LCD_Write(8,j, text[j].encode("UTF-8"))
	time.sleep(1)

