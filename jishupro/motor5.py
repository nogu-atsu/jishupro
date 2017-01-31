#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep


class Motor:
    def __init__(self,gpio1,gpio2):
        self.gpio1 = gpio1
        self.gpio2 = gpio2
        self.state = 0
        self.abs_rot = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio1,GPIO.OUT)
        GPIO.setup(gpio2,GPIO.OUT)
        GPIO.output(gpio1,0)#state[0]
        GPIO.output(gpio2,0)
        
    def l_rotate(self):
        states =  [[0,0],[1,0],[1,1],[0,1]]
        self.state = (self.state+1)%4
        GPIO.output(self.gpio1,states[self.state][0])
        GPIO.output(self.gpio2,states[self.state][1])
        
    def r_rotate(self):
        states =  [[0,0],[1,0],[1,1],[0,1]]
        self.state = (self.state-1)%4
        GPIO.output(self.gpio1,states[self.state][0])
        GPIO.output(self.gpio2,states[self.state][1])

    def rotate(self,sign):
        states =  [[0,0],[1,0],[1,1],[0,1]]
        self.state = (self.state+sign)%4
        self.abs_rot += sign
        GPIO.output(self.gpio1,states[self.state][0])
        GPIO.output(self.gpio2,states[self.state][1])

#移動の向きはモータのある側を下にした時
#左がm1,右がm2
def up(m1,m2,step,palse_width=0.01):
    for i in range(step):
        m1.l_rotate()
        m2.r_rotate()
        sleep(palse_width)

def down(m1,m2,step,palse_width=0.01):
    for i in range(step):
        m1.r_rotate()
        m2.l_rotate()
        sleep(palse_width)

def left(m1,m2,step,palse_width=0.01):
    for i in range(step):
        m1.r_rotate()
        m2.r_rotate()
        sleep(palse_width)

def right(m1,m2,step,palse_width=0.01):
    for i in range(step):
        m1.l_rotate()
        m2.l_rotate()
        sleep(palse_width)

if __name__=="__main__":
    m1 = Motor(6,13)
    m2 = Motor(19,26)

    try:
        for i in range(5):
            up(m1,m2,20)
            left(m1,m2,20)
            down(m1,m2,20)
            right(m1,m2,20)
    except KeyboardInterrupt:
        pass
    
    GPIO.cleanup()
