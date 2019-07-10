from ctypes import *

hello = cdll.LoadLibrary('./hello.so')
hello.Hello()

led = cdll.LoadLibrary('/home/pi/QSS003_python//led.so')
led.led()

#LTC1865 = cdll.LoadLibrary('/home/pi/QSS003_python//LTC1865.so')
#LTC1865.LTC_init(0, 0)
#data = LTC1865.LTC_Read(0)
#print(data)
