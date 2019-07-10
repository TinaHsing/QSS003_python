from ctypes import *

m = cdll.LoadLibrary('./hello.so')
m.Hello()
