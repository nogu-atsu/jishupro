import RPi.GPIO as GPIO
from time import sleep

a = 19
b = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(a, GPIO.OUT)
GPIO.setup(b, GPIO.OUT)


try:
    for i in range(200):
        GPIO.output(a, GPIO.LOW)
        GPIO.output(b, GPIO.LOW)
        sleep(0.002)
        GPIO.output(a, GPIO.HIGH)
        GPIO.output(b, GPIO.LOW)
        sleep(0.002)
        GPIO.output(a, GPIO.HIGH)
        GPIO.output(b, GPIO.HIGH)
        sleep(0.002)
        GPIO.output(a, GPIO.LOW)
        GPIO.output(b, GPIO.HIGH)
        sleep(0.002)
    for i in range(100):
        GPIO.output(a, GPIO.LOW)
        GPIO.output(b, GPIO.LOW)
        sleep(0.002)
        GPIO.output(a, GPIO.LOW)
        GPIO.output(b, GPIO.HIGH)
        sleep(0.002)
        GPIO.output(a, GPIO.HIGH)
        GPIO.output(b, GPIO.HIGH)
        sleep(0.002)
        GPIO.output(a, GPIO.HIGH)
        GPIO.output(b, GPIO.LOW)
        sleep(0.002)
except KeyboardInterrupt:
    pass

GPIO.cleanup()
