import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)


t1 = time.time()
for i in range (0,100):
	GPIO.output(11, True)
	GPIO.output(11, False)
t2 = time.time()
dt = (t2-t1)*10000
head = "100:"
print(head+str(dt))
t1 = time.time()
for i in range (0,1000):
	GPIO.output(11, True)
	GPIO.output(11, False)
t2 = time.time()
dt = (t2-t1)*1000
head = "1000:"
print(head+str(dt))
t1 = time.time()
for i in range (0,10000):
	GPIO.output(11, True)
	GPIO.output(11, False)
t2 = time.time()
dt = (t2-t1)*100
head = "10000:"
print(head+str(dt))
t1 = time.time()
for i in range (0,100000):
	GPIO.output(11, True)
	GPIO.output(11, False)
t2 = time.time()
dt = (t2-t1)*10
head = "100000:"
print(head+str(dt))


