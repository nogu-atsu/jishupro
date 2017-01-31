import RPi.GPIO as GPIO
from time import sleep

a1 = 6
b1 = 13
a2 = 19
b2 = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(a1, GPIO.OUT)
GPIO.setup(b1, GPIO.OUT)
GPIO.setup(a2, GPIO.OUT)
GPIO.setup(b2, GPIO.OUT)

output_a1 = [1,1,0,0]
output_b1 = [0,1,1,0]

output_a2 = [0,1,1,0]
output_b2 = [1,1,0,0] 
try:
    for i in range(200):
        GPIO.output(a1, output_a1[i%4])
        GPIO.output(b1, output_b1[i%4])
        GPIO.output(a2, output_a1[i%4])
        GPIO.output(b2, output_b1[i%4])        
        sleep(0.002)
    for i in range(200):
        GPIO.output(a1, output_a2[i%4])
        GPIO.output(b1, output_b2[i%4])
        GPIO.output(a2, output_a2[i%4])
        GPIO.output(b2, output_b2[i%4])
        sleep(0.002)
except KeyboardInterrupt:
    pass

GPIO.cleanup()
