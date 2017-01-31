from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(320, 240))

# allow the camera to warmup
time.sleep(0.1)
abs_pos = 0
images = []
poss=[]
print "ready"
for i,frame in enumerate(camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)):
    image = frame.array
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)[:,::-1]
    thre = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,2)
    print i,
    if i == 1:
        pre_thre = thre[90:150,:]
        images.append(gray)
        poss.append(abs_pos)
        cv2.imshow("Frame", thre)
    elif i>1:
        res = cv2.matchTemplate(thre,pre_thre,cv2.TM_CCOEFF)
        pre_thre = thre[90:150,:]
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        bottom_right = (max_loc[0] + 320, max_loc[1] + 60)
        abs_pos += max_loc[1]-90
        images.append(gray)
        poss.append(abs_pos)
        print abs_pos
        #cv2.rectangle(thre,max_loc, bottom_right, 128, 2)
        cv2.imshow("Frame", thre)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    if i==120:
        break
poss = np.array(poss)
print poss,np.argmax(poss),np.argmin(poss)
images = np.array(images)
np.save("images.npy",images)
sudoku_img = np.zeros((240+np.max(poss)-np.min(poss),320),dtype=np.int32)
overlap = np.zeros((240+np.max(poss)-np.min(poss),1),dtype=np.int32)
sudoku_img[0:90,:] += images[np.argmax(poss)][0:90,:]
overlap[0:90,:]+=1
sudoku_img[-90:,:] += images[np.argmin(poss)][-90:,:]
overlap[-90:,:]+=1
for i in range(120):
    pos = np.max(poss)-poss[i]
    sudoku_img[pos+90:pos+150,:] += images[i][90:150,:]
    overlap[pos+90:pos+150,:]+=1
sudoku_img = sudoku_img//overlap
#cv2.imshow("Frame",cv2.adaptiveThreshold(sudoku_img.astype(np.uint8),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,2))
#cv2.imshow("Frame",sudoku_img.astype(np.uint8))
#cv2.waitKey(0)
np.save("sudoku_cap",cv2.adaptiveThreshold(sudoku_img.astype(np.uint8),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,5,2))
#plt.imshow(cv2.adaptiveThreshold(sudoku_img.astype(np.uint8),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,5,2),"gray")
plt.imshow(sudoku_img.astype(np.uint8),"gray")
plt.show()
