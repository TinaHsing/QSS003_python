import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

t1 = time.time()
for i in xrange (0,10000):
	GPIO.output(11, True)
	GPIO.output(11, False)
t2 = time.time()
dt = t2-t1
print(dt)


