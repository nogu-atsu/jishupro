#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep
from motor5 import Motor
import threading
import numpy as np
#正方形に動く

def rotate(_rotate,step,_time):#time秒でrotateをstep回
    for s in range(abs(step)):
        _rotate((step>0)*2-1)
        sleep(_time/abs(step))
    
def move(m1,m2,vec):#vecは2次元のndarray,vec(mm)
    _vec=vec/0.18
    m1_step = int(_vec[0]+_vec[1])
    m2_step = int(_vec[0]-_vec[1])
    _time = max(abs(m1_step),abs(m2_step))*0.005
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
        
        for i in range(5):
            move(m1,m2,np.array([20,0]))
            move(m1,m2,np.array([0,20]))
            move(m1,m2,np.array([-20,0]))
            move(m1,m2,np.array([0,-20]))
        
                
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()
    
