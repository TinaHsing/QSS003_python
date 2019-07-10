from ctypes import *

#m = cdll.LoadLibrary('./hello.so')
#m.Hello()

#m = cdll.LoadLibrary('/home/pi/QSS003_python//led.so')
#m.led()

LTC1865 = cdll.LoadLibrary('/home/pi/QSS003_python//LTC1865.so')
LTC1865.init(0, 0)
print LTC1865.Read(0)
