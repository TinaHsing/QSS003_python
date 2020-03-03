import pigpio
import RPi.GPIO as GPIO
import time

GATE_PIN1 = 7
GATE_PIN2 = 15
PWM_LED_PIN = 18
PWM_LED_PIN2 = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(GATE_PIN1, GPIO.OUT)
GPIO.setup(GATE_PIN2, GPIO.OUT)
GPIO.output(GATE_PIN1, GPIO.HIGH)	#close
#GPIO.output(GATE_PIN1, GPIO.LOW)	#open
GPIO.output(GATE_PIN2, GPIO.HIGH)	#close
#GPIO.output(GATE_PIN2, GPIO.LOW)	#open

PWM_FREQ = 500
DUTY = 100000	#0~1000000
DUTY2 = 100000

pi = pigpio.pi()
pi.hardware_PWM(PWM_LED_PIN, PWM_FREQ, DUTY)
pi.hardware_PWM(PWM_LED_PIN2, PWM_FREQ, DUTY2)

while(1):
        GPIO.output(GATE_PIN1, GPIO.LOW)
        GPIO.output(GATE_PIN2, GPIO.LOW)
        time.sleep(3)
        GPIO.output(GATE_PIN1, GPIO.HIGH)
        GPIO.output(GATE_PIN2, GPIO.HIGH)
        time.sleep(3)
