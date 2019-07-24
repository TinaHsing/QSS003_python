from ctypes import *

ledctrl1 = 8
ledctrl2 = 1
ledcrtl3 = 4
spec_st = 22
spec_clk = 23

C12880 = cdll.LoadLibrary('/home/pi/QSS003_python//C12880.so')
#C12880.LTC_Init(0, 0)
#data = C12880.LTC_Read(0)
#print(data)
C12880.Setup(spec_st, spec_clk)

C12880.LED_Init(ledctrl1)	#init led driver 1
C12880.LED_Init(ledctrl2)	#init led driver 2   
C12880.LED_Init(ledctrl3)	#init led driver 3
C12880.LED_Set(ledctrl1, 25) # set LED driver1 current to 25mA
C12880.LED_Set(ledctrl2, 10) # set LED driver2 current to 10mA
C12880.LED_Set(ledctrl3, 4) # set LED driver3 current to 4mA


data = (c_uint * 288)()




C12880.ReadSpectrometer(1, 10, data)
for i in range(0,288):
	print(data[i])

C12880.LCD_Init()
C12880.LCD_Clear()
C12880.LCD_Write(0, 0, "     Hello World")
C12880.LCD_Write(1, 6, "1234567890")

