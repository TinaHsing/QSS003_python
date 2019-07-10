from ctypes import *

#m = cdll.LoadLibrary('./hello.so')
#m.Hello()

#m = cdll.LoadLibrary('/home/pi/QSS003_python//led.so')
#m.led()

LTC1865 = cdll.LoadLibrary('/home/pi/QSS003_python//LTC1865.so')
LTC1865.LTC_init(0, 0)
data = LTC1865.LTC_Read(0)
print(data)
