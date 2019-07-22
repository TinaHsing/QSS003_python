from ctypes import *

hello = cdll.LoadLibrary('./hello.so')
hello.Hello()

#led = cdll.LoadLibrary('/home/pi/QSS003_python//led.so')
#led.led()

ltc = cdll.LoadLibrary('/home/pi/QSS003_python//LTC1865.so')
ltc.LTC_init(0, 0)
data = ltc.LTC_Read(0)
print(data)

C12880 = cdll.LoadLibrary('/home/pi/QSS003_python//C12880.so')
C12880.setup(1,2,3,4)
data = (c_uint * 288)()
C12880.readSpectrometer(1,10,data)
for i in range(0,288):
	print(data[i])
