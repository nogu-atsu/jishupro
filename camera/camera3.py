from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(320, 240))

# allow the camera to warmup
time.sleep(0.1)
for i,frame in enumerate(camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)):
    image = frame.array
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    thre = cv2.adaptiveThreshold(gray[:,::-1],255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    print i,thre.shape
    cv2.imshow("Frame", thre)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
