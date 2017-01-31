import RPi.GPIO as GPIO
from time import sleep

a = 19
b = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(a, GPIO.OUT)
GPIO.setup(b, GPIO.OUT)
output_a = [0,1,1,0]
output_b = [0,0,1,1]

try:
    for i in range(200):
        GPIO.output(a, output_a[i%4])
        GPIO.output(b, output_b[i%4])
        sleep(0.002)
except KeyboardInterrupt:
    pass

GPIO.cleanup()
