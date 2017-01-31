import io
import picamera
import cv2
import time
import numpy as np

stream = io.BytesIO()

CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

camera = picamera.PiCamera() 
camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
camera.framerate = 80
time.sleep(2)
for i in xrange(100):    
    camera.capture(stream, format='jpeg')
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    image = cv2.imdecode(data, 1)
    print image.shape
    #cv2.imshow('image',image)
    cv2.waitKey(1)
    stream.seek(0)
    print "captured %d" % (i)
