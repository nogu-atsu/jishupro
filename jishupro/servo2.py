#!/usr/bin/env python
# -*- coding: utf-8 -*-
#擬似PWM制御信号を生成

import RPi.GPIO as GPIO
import time

# 初期設定
GPIO.setmode(GPIO.BCM)

# GPIO 14 を出力に設定
GPIO.setup(14, GPIO.OUT)
"""
# PWM 設定
freq = 50 # Hz (PWM のパルスを一秒間に 50 個生成)
duty = 0.0 # デューティー比 0.0 で出力開始 (パルス内に占める HIGH 状態の時間が 0.0 %)
pwm = GPIO.PWM(14, freq)
pwm.start(2.5)

try:
    # デューティー比 (duty cycle) を 0..100 の範囲で変化 (Ctrl-C 待ち)
    while True:
        duty = (duty + 1) % 11
        print 3+duty/10.*8.5
        pwm.ChangeDutyCycle(3+duty/10.*8.5)
        time.sleep(0.5)
except:
    print "interrupted"
finally:
    # 後片付け
    pwm.stop()
    GPIO.cleanup()
"""

try:
    for i in range(100):
        duty = 0.00055 + i*0.00175/100
        GPIO.output(14,1)
        time.sleep(duty)
        GPIO.output(14,0)
        time.sleep(0.0199-duty)
except KeyboardInterrupt:
    pass
GPIO.cleanup()
        
