from ctypes import *

C12880 = cdll.LoadLibrary('/home/pi/QSS003_python//C12880.so')
C12880.LTC_init(0, 0)
data = C12880.LTC_Read(0)
print(data)

C12880.setup(1, 2, 3, 4)
data = (c_uint * 288)()
C12880.readSpectrometer(1, 10, data)
for i in range(0,288):
	print(data[i])

C12880.LED_init(1)
C12880.LED_set(1, 25)
