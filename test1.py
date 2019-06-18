import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

t1 = time.time()
for i in range (0,100):
	GPIO.output(11, True)
	GPIO.output(11, False)
t2 = time.time()
dt = t2-t1
print(100:)
print(dt)
t1 = time.time()
for i in range (0,1000):
	GPIO.output(11, True)
	GPIO.output(11, False)
t2 = time.time()
dt = t2-t1
print(1000:)
print(dt)
t1 = time.time()
for i in range (0,10000):
	GPIO.output(11, True)
	GPIO.output(11, False)
t2 = time.time()
dt = t2-t1
print(10000:)
print(dt)
t1 = time.time()
for i in range (0,100000):
	GPIO.output(11, True)
	GPIO.output(11, False)
t2 = time.time()
dt = t2-t1
print(100000:)
print(dt)


