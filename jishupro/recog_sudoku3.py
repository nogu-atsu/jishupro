# -*- coding: utf-8 -*-
import cv2
import numpy as np
import math
from sudoku_maker import Sudoku_Maker
from scipy import stats

def Recog_Sudoku(mode=0,image=None):
    IMAGE_SIZE = 32
    SUDOKU_SIZE= 9
    pers_size = IMAGE_SIZE*SUDOKU_SIZE
    N_MIN_ACTVE_PIXELS = 100
    
    #sort the corners to remap the image
    def getOuterPoints(rcCorners):
        ar = rcCorners[0:4,0,:]
        center = np.average(ar,axis=0)
        #print center,ar
        sort=[0,0,0,0]
        for i in range(4):
            sort[(ar[i]<center)[0]+(ar[i]<center)[1]*2]=i
        return ar[sort]
    if mode == 0:
        im,digits = Sudoku_Maker()
        im = (im*255).astype(np.uint8)
    else:
        im = cv2.imread(image)
        im = np.clip((im+stats.truncnorm.rvs(-1,1,size = im.shape)*50).astype(np.uint8),0,255)
        digits = 0
    #size of the image (height, width)
    h, w = im.shape[:2]
    im = cv2.resize(im,(w*600//h,600))
    gray = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
    gauss = cv2.GaussianBlur(gray, (5,5), 1)
    a_th = cv2.adaptiveThreshold(gauss,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,5,2)

    
    #find the countours
    contour = cv2.findContours(a_th,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if len(contour)==3:#for oepncv3-1
        _,contours0,hierarchy =contour
    else:#for opencv2-4
        contours0,hierarchy =contour
    #_,contours0,hierarchy= cv2.findContours( a_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #biggest rectangle
    size_rectangle_max = 0;
    for i in range(len(contours0)):
        #aproximate countours to polygons
        approximation = cv2.approxPolyDP(contours0[i], 4, True)
        #has the polygon 4 sides?
        if not len(approximation)==4:
            continue;
        #is the polygon convex ?
        if not cv2.isContourConvex(approximation):
            continue; 
        #area of the polygon
        size_rectangle = cv2.contourArea(approximation)
        #store the biggest
        if size_rectangle> size_rectangle_max:
            size_rectangle_max = size_rectangle 
            big_rectangle = approximation
            
    
    #show the best candidate
    approximation = big_rectangle
    #point to remap
    points1 = np.array([[pers_size,pers_size],[0,pers_size],[pers_size,0],[0,0]],dtype=np.float32)    
    outerPoints = getOuterPoints(approximation)
    points2 = np.array(outerPoints,np.float32)
    if np.sum(points2==599.)>0:
        return None,None,None
    
    #Transformation matrix
    pers = cv2.getPerspectiveTransform(points2,points1);
    
    #remap the image
    warp = cv2.warpPerspective(im, pers, (pers_size,pers_size));
    warp_gray = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
    warp_th = cv2.adaptiveThreshold(warp_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,2)
    sudoku = np.zeros((81,32,32))
    for i in range(9):
        for j in range(9):
            sudoku[i*9+j] =warp_th[i*32:(i+1)*32,j*32:(j+1)*32]
    
    return sudoku,IMAGE_SIZE,digits



if __name__=="__main__":
    sudoku,IMAGE_SIZE,_=Recog_Sudoku(mode=1,image="DSC_0289.jpg")
    if sudoku==None:
        print("failed")
    else:
        sudoku2 = sudoku.reshape(81,IMAGE_SIZE,IMAGE_SIZE)
        sudoku3 = np.zeros((9*IMAGE_SIZE,9*IMAGE_SIZE))
        for i in range(9):
            for j in range(9):
                sudoku3[i*IMAGE_SIZE:(i+1)*IMAGE_SIZE,j*IMAGE_SIZE:(j+1)*IMAGE_SIZE]=sudoku2[i*9+j]
        plt.imshow(sudoku3)
        plt.show()
