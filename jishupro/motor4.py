#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep

#右から順に接続
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
#移動の向きはモータのある側を下にした時
def up(a1,b1,a2,b2,step):
    output_a = [0,1,1,0]
    output_b = [1,1,0,0]
    for i in range(step):
        GPIO.output(a1, output_a[i%4])
        GPIO.output(b1, output_b[i%4])
        GPIO.output(a2, output_a[i%4])
        GPIO.output(b2, output_b[i%4])
        sleep(0.005)

def down(a1,b1,a2,b2,step):
    output_a = [1,1,0,0]
    output_b = [0,1,1,0]
    for i in range(step):
        GPIO.output(a1, output_a[i%4])
        GPIO.output(b1, output_b[i%4])
        GPIO.output(a2, output_a[i%4])
        GPIO.output(b2, output_b[i%4])
        sleep(0.005)

def left(a1,b1,a2,b2,step):
    output_a1 = [1,1,0,0]
    output_b1 = [0,1,1,0]
    output_a2 = [0,1,1,0]
    output_b2 = [1,1,0,0]
    for i in range(step):
        GPIO.output(a1, output_a1[i%4])
        GPIO.output(b1, output_b1[i%4])
        GPIO.output(a2, output_a2[i%4])
        GPIO.output(b2, output_b2[i%4])
        sleep(0.005)

def right(a1,b1,a2,b2,step):
    output_a1 = [0,1,1,0]
    output_b1 = [1,1,0,0]
    output_a2 = [1,1,0,0]
    output_b2 = [0,1,1,0]
    for i in range(step):
        GPIO.output(a1, output_a1[i%4])
        GPIO.output(b1, output_b1[i%4])
        GPIO.output(a2, output_a2[i%4])
        GPIO.output(b2, output_b2[i%4])
        sleep(0.005)

try:
    for i in range(5):
        up(a1,b1,a2,b2,100)
        left(a1,b1,a2,b2,100)
        down(a1,b1,a2,b2,100)
        right(a1,b1,a2,b2,100)
    
except KeyboardInterrupt:
    pass

GPIO.cleanup()
