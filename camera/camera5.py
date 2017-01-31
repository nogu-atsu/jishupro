from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
from classifier2 import CNN
import threading
from motor8 import Plotter
from sudoku2 import Solver
def move(plotter):    
    for i in range(160):
        vec = np.array([0,-1])
        plotter(vec,step_time=0.01)
        print plotter.get_pos()
    for i in range(160):
        vec = np.array([0,1])
        plotter(vec,step_time=0.01)
        print plotter.get_pos()
    plotter.stop()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 6
rawCapture = PiRGBArray(camera, size=(320, 240))

# allow the camera to warmup
time.sleep(0.1)
images = []
print "ready"
plotter = Plotter()

thread1 = threading.Thread(target = move,args=(plotter,))
thread1.start()
for i,frame in enumerate(camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)):
    image = frame.array
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)[:,::-1]
    print i
    images.append(gray)
    #cv2.imshow("Frame", gray)
    #key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if i==100:
        break
thread1.join()
images_th = [cv2.adaptiveThreshold(images[i].astype(np.uint8),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,5) for i in range(100)]
join_img = images[0]
overlap = np.ones((len(join_img),1),dtype=np.int32)
for i in range(1,100):
    print i
    join_th = cv2.adaptiveThreshold((join_img/overlap).astype(np.uint8),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,5)
    res = cv2.matchTemplate(join_th,images_th[i][90:150,:],cv2.TM_CCOEFF)
    _,_,_,max_loc = cv2.minMaxLoc(res)
    max_loc = max_loc[1]
    if max_loc<=90:
        tmp = np.zeros((len(join_img)+90-max_loc,320),dtype=np.int32)
        tmp[:150,:]=images[i][:150,:]
        tmp[180-max_loc:,:]+=join_img[90:,:]
        join_img = tmp
        tmp = np.zeros((len(join_img),1),dtype=np.int32)
        tmp[:150,:]+=1
        tmp[180-max_loc:,:]+=overlap[90:,:]
        overlap = tmp
    elif max_loc>=len(join_img)-150:
        leng = len(join_img)
        tmp = np.zeros((leng+max_loc-leng+150,320),dtype=np.int32)
        tmp[:len(join_img)-90,:]=join_img[:-90,:]
        tmp[max_loc:,:]+=images[i][90:,:]
        join_img = tmp
        tmp = np.zeros((len(join_img),1),dtype=np.int32)
        tmp[:leng-90,:]+=overlap[:-90,:]
        tmp[max_loc:,:]+=1
        overlap = tmp
    else:
        join_img[max_loc:max_loc+60,:] += images[i][90:150,:]
        overlap[max_loc:max_loc+60,:]+=1
join_img = join_img/overlap
sudoku = cv2.adaptiveThreshold(join_img.astype(np.uint8),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,5)
sudoku = sudoku[60:-60,:]
sum0 = np.sum(sudoku,axis=0)/255.
sum1 = np.sum(sudoku,axis=1)/255.
thres0 = (np.max(sum0)+np.min(sum0))/2
thres1 = (np.max(sum1)+np.min(sum1))/2
s0 = np.where(sum0<thres0)[0]
s1 = np.where(sum1<thres1)[0]
sudoku = sudoku[s1[0]:s1[-1],s0[0]:s0[-1]]
#np.save("join_sudoku.npy",sudoku)
#plt.imshow(sudoku,"gray")
#plt.show()
sudoku = cv2.resize(sudoku,(32*9,32*9))
sudoku = np.array([sudoku[i//9*32:i//9*32+32,i%9*32:i%9*32+32] for i in range(81)])
"""
for i in range(81):
    plt.subplot(9,9,i+1)
    plt.imshow(sudoku[i],"gray")
    plt.axis("off")
plt.show()

#plt.imshow(sudoku,"gray")
#plt.show()
"""
cnn = CNN()

sudoku = sudoku.reshape(81,32,32,1)
digits = cnn(sudoku).reshape(9,9)
print(digits)
    
"""
digits = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
digits = np.array([int(d) for d in digits])
#ans = Solver(digits)
"""
