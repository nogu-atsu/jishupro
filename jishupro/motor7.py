#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep
from motor5 import Motor
import threading
import numpy as np
import math

#円形に動く

def rotate(_rotate,step,_time):#time秒でrotateをstep回
    for s in range(abs(step)):
        _rotate((step>0)*2-1)
        sleep(_time/abs(step))
    
def move(m1,m2,vec):#vecは2次元のndarray,vec(mm)
    _vec=vec/0.18
    m1_step = int(_vec[0]+_vec[1])
    m2_step = int(_vec[0]-_vec[1])
    _time = max(abs(m1_step),abs(m2_step))*0.002
    thread1 = threading.Thread(target=rotate,args=(m1.rotate,m1_step,_time))
    thread2 = threading.Thread(target=rotate,args=(m2.rotate,m2_step,_time))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

if __name__ == '__main__':
    m1 = Motor(6,13)
    m2 = Motor(19,26)
    try:
        #move(m1,m2,np.array([0,30]))
        
        for i in range(500):
            vec = 50*np.array([math.cos((i+1)*np.pi/50)-math.cos(i*np.pi/50),
                            math.sin((i+1)*np.pi/50)-math.sin(i*np.pi/50)])
            move(m1,m2,vec)
        
                
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()
    
