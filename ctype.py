from ctypes import *

#m = cdll.LoadLibrary('./hello.so')
#m.Hello()

m = cdll.LoadLibrary('/home/pi/QSS003_python//led.so')
m.led()
