#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep
from motor5 import Motor
import threading
import numpy as np
import math
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):
        self.m1 = Motor(6,13)
        self.m2 = Motor(19,26)
        

    def rotate(self,_rotate,step,_time):#time秒でrotateをstep回
        for s in range(abs(step)):
            _rotate((step>0)*2-1)
            sleep(_time/abs(step))
    
    def __call__(self,vec,step_time = 0.002):#vecは2次元のndarray,vec(mm)
        _vec=vec/0.18
        m1_step = int(_vec[0]+_vec[1])
        m2_step = int(_vec[0]-_vec[1])
        _time = max(abs(m1_step),abs(m2_step))*step_time
        thread1 = threading.Thread(target=self.rotate,args=(self.m1.rotate,m1_step,_time))
        thread2 = threading.Thread(target=self.rotate,args=(self.m2.rotate,m2_step,_time))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    def get_pos(self):#mm単位で返す
        return np.array([(self.m1.abs_rot+self.m2.abs_rot),(self.m1.abs_rot-self.m2.abs_rot)])*0.09
    def stop(self):
        GPIO.cleanup()
    
if __name__ == '__main__':
    plotter = Plotter()
    pos=[]
    try:
        """
        for i in range(100):
            vec = 30*np.array([math.cos((i+1)*np.pi/50)-math.cos(i*np.pi/50),
                            math.sin((i+1)*np.pi/50)-math.sin(i*np.pi/50)])
            plotter(vec)
            pos.append(plotter.get_pos())
            print plotter.get_pos(),str("mm")
        """
        for t in range(5):
            for i in range(160):
                vec = np.array([0,-1])
                plotter(vec,step_time=0.01)
                print plotter.get_pos()
            for i in range(160):
                vec = np.array([0,1])
                plotter(vec,step_time=0.01)
                print plotter.get_pos()
            
    except KeyboardInterrupt:
        pass
    plotter.stop()
    """
    pos = np.transpose(np.array(pos))
    plt.plot(pos[0],pos[1],"bo")
    plt.show()
    """
