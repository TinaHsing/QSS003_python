from ctypes import *

hello = cdll.LoadLibrary('./hello.so')
hello.Hello()

led = cdll.LoadLibrary('/home/pi/QSS003_python//led.so')
led.led()

ltc = cdll.LoadLibrary('/home/pi/QSS003_python//LTC1865.so')
ltc.LTC_init(0, 0)
data = ltc.LTC_Read(0, 0)
print(data)
