from ctypes import *

#m = cdll.LoadLibrary('./hello.so')
#m.Hello()

m = cdll.LoadLibrary('./led.so')
m.led()
