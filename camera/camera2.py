#very slow
import io
import picamera
import cv2
import time
import numpy as np
import picamera.array

CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

camera = picamera.PiCamera() 
camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
time.sleep(2)
stream = picamera.array.PiRGBArray(camera)
for i in xrange(100):
    s = time.time()
    camera.capture(stream, format='bgr')
    e = time.time()
    print e-s
    image = stream.array
    print image.shape
    #cv2.imshow('image',image)
    #cv2.waitKey(1)
    stream.seek(0)
    print "captured %d" % (i)
