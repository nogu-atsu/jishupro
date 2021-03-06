from motor8 import *
import RPi.GPIO as GPIO
from servo import *
import time
class Draw_num:
    def __init__(self):
        self.plotter = Plotter()
        self.pen = Pen()
    def __call__(self,num):
        if num==1:
            self.one()
        elif num==2:
            self.two()
        elif num==3:
            self.three()
        elif num==4:
            self.four()
        elif num==5:
            self.five()
        elif num==6:
            self.six()
        elif num==7:
            self.seven()
        elif num==8:
            self.eight()
        elif num==9:
            self.nine()
    def one(self):
        self.plotter(np.array([0,6]))
        self.pen.down()
        time.sleep(0.5)
        self.plotter(np.array([0,-12]))
        self.pen.up()
        time.sleep(0.5)
        self.plotter(np.array([0,6]))
    def two(self):
        self.plotter(np.array([-3.96,6]))
        self.pen.down()
        time.sleep(0.5)
        self.plotter(np.array([7.92,0]))
        self.plotter(np.array([0,-6]))
        self.plotter(np.array([-7.92,0]))
        self.plotter(np.array([0,-6]))
        self.plotter(np.array([7.92,0]))
        self.pen.up()
        time.sleep(0.5)
        self.plotter(np.array([-3.96,6]))
    def three(self):
        self.plotter(np.array([-3.96,6]))
        self.pen.down()
        time.sleep(0.5)
        self.plotter(np.array([7.92,0]))
        self.plotter(np.array([0,-6]))
        self.plotter(np.array([-7.92,0]))
        self.plotter(np.array([7.92,0]))
        self.plotter(np.array([0,-6]))
        self.plotter(np.array([-7.92,0]))
        self.pen.up()
        time.sleep(0.5)
        self.plotter(np.array([3.96,6]))
    def four(self):
        self.plotter(np.array([-3.96,6]))
        self.pen.down()
        time.sleep(0.5)
        self.plotter(np.array([0,-6]))
        self.plotter(np.array([7.92,0]))
        self.plotter(np.array([0,6]))
        self.plotter(np.array([0,-12]))
        self.pen.up()
        time.sleep(0.5)
        self.plotter(np.array([-3.96,6]))
    def five(self):
        self.plotter(np.array([-3.96,6]))
        self.pen.down()
        time.sleep(0.5)
        self.plotter(np.array([0,-6]))
        self.plotter(np.array([7.92,0]))
        self.plotter(np.array([0,-6]))
        self.plotter(np.array([-7.92,0]))
        self.pen.up()
        time.sleep(0.5)
        self.plotter(np.array([0,12]))
        self.pen.down()
        time.sleep(0.5)
        self.plotter(np.array([7.92,0]))
        self.pen.up()
        time.sleep(0.5)
        self.plotter(np.array([-3.96,-6]))
    def six(self):
        self.plotter(np.array([3.96,6]))
        self.pen.down()
        time.sleep(0.5)
        self.plotter(np.array([-7.92,0]))
        self.plotter(np.array([0,-12]))
        self.plotter(np.array([7.92,0]))
        self.plotter(np.array([0,6]))
        self.plotter(np.array([-7.92,0]))
        self.pen.up()
        time.sleep(0.5)
        self.plotter(np.array([3.96,0]))
    def seven(self):
        self.plotter(np.array([-3.96,0]))
        self.pen.down()
        time.sleep(0.5)
        self.plotter(np.array([0,6]))
        self.plotter(np.array([7.92,0]))
        self.plotter(np.array([0,-12]))
        self.pen.up()
        time.sleep(0.5)
        self.plotter(np.array([-3.96,6]))
    def eight(self):
        self.plotter(np.array([-3.96,0]))
        self.pen.down()
        time.sleep(0.5)
        self.plotter(np.array([0,6]))
        self.plotter(np.array([7.92,0]))
        self.plotter(np.array([0,-6]))
        self.plotter(np.array([-7.92,0]))
        self.plotter(np.array([0,-6]))
        self.plotter(np.array([7.92,0]))
        self.plotter(np.array([0,6]))
        self.plotter(np.array([-7.92,0]))
        self.pen.up()
        time.sleep(0.5)
        self.plotter(np.array([3.96,0]))
    def nine(self):
        self.plotter(np.array([3.96,0]))
        self.pen.down()
        time.sleep(0.5)
        self.plotter(np.array([-7.92,0]))
        self.plotter(np.array([0,6]))
        self.plotter(np.array([7.92,0]))
        self.plotter(np.array([0,-12]))
        self.plotter(np.array([-7.92,0]))
        self.pen.up()
        time.sleep(0.5)
        self.plotter(np.array([3.96,6]))
    def stop(self):
        self.pen.stop()
        self.plotter.stop()

if __name__=="__main__":
    plotter = Plotter()
    dn = Draw_num()
    dn(1)
    plotter(np.array([12,0]))
    dn(2)
    plotter(np.array([12,0]))
    dn(3)
    plotter(np.array([12,0]))
    dn(4)
    plotter(np.array([12,0]))
    dn(5)
    plotter(np.array([12,0]))
    dn(6)
    plotter(np.array([12,0]))
    dn(7)
    plotter(np.array([12,0]))
    dn(8)
    plotter(np.array([12,0]))
    dn(9)
    dn.stop()
