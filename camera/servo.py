#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

class Pen:
    def __init__(self):
        # 初期設定
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        
        # PWM 設定
        freq = 50 # Hz (PWM のパルスを一秒間に 50 個生成)
        duty = 0.0 # デューティー比 0.0 で出力開始 (パルス内に占める HIGH 状態の時間が 0.0 %)
        self.pwm = GPIO.PWM(18, freq)
        self.pwm.start(4.3)
    def up(self):
        self.pwm.ChangeDutyCycle(4.3)
    def down(self):
        self.pwm.ChangeDutyCycle(9.4)
    def stop(self):
        self.pwm.stop()
        GPIO.cleanup()
        
if __name__=="__main__":
    pen = Pen()
    try:
        while True:
            pen.up()
            time.sleep(1.0)
            pen.down()
            time.sleep(1.0)
    except:
        print "interrupted"
    # 後片付け
    pen.stop()
