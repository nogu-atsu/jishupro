from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))


cascade_path = "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_path)


# allow the camera to warmup
time.sleep(0.1)
for i,frame in enumerate(camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)):
    image = frame.array
    #print i,image.shape
    key = cv2.waitKey(1)
    
    image_gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    #print image_gray.shape
    #cv2.imshow("Frame", image_gray)
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
    image_output = image
    #print len(facerect)
    if len(facerect) > 0:
        for rect in facerect:
            cv2.rectangle(image_output, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), (255,255,255), thickness=2)
        print "found" 
    cv2.imshow("Frame", image_output)
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
