import pigpio
import RPi.GPIO as GPIO
import time

GATE_PIN = 15
PWM_LED_PIN = 18
PWM_LED_PIN2 = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(GATE_PIN, GPIO.OUT)

GPIO.output(GATE_PIN, GPIO.HIGH)	#close
#GPIO.output(GATE_PIN, GPIO.LOW)	#open

PWM_FREQ = 500
DUTY = 100000	#0~1000000
DUTY2 = 100000

pi = pigpio.pi()
#pi.hardware_PWM(PWM_LED_PIN, PWM_FREQ, DUTY)
pi.hardware_PWM(PWM_LED_PIN2, PWM_FREQ, DUTY2)

#
for i in range(0,11):
        pi.hardware_PWM(PWM_LED_PIN, PWM_FREQ, DUTY*i)
        GPIO.output(GATE_PIN, GPIO.LOW)
        time.sleep(10)
        GPIO.output(GATE_PIN, GPIO.HIGH)
        time.sleep(5)
##
