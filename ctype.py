from ctypes import *

m = cdll.LoadLibrary('./test.so')
m.Hello()