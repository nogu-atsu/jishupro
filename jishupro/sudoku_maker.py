# -*- coding: utf-8 -*-
import sys
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import numpy as np
import json
#from scipy import ndimage
import cv2

def Sudoku_Maker():
    ims = np.load("number_images.npy")
    #digits = np.random.randint(0,10,size=[9,9])
    digits = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    sudoku = np.load("waku.npy")
    
    for i in range(9):
        for j in range(9):
            if digits[i][j]!=0:
                sudoku[860+i*410-len(ims[digits[i][j]-1])//2:860+i*410+len(ims[digits[i][j]-1])-len(ims[digits[i][j]-1])//2,860+j*410-len(ims[digits[i][j]-1][0])//2:860+j*410+len(ims[digits[i][j]-1][0])-len(ims[digits[i][j]-1][0])//2,:]=ims[digits[i][j]-1]/255
    
    
    points1 = np.array([[25,25],[25,1225],[1225,20],[1225,1225]],dtype=np.float32)
    points2 = np.array([[200,200],[200,4800],[4800,200],[4800,4800]],dtype=np.float32)+np.random.randint(-100,100,[4,2]).astype(np.float32)
    pers = cv2.getPerspectiveTransform(points2,points1);
    sudoku = cv2.warpPerspective(sudoku, pers, (1250,1250));
    sudoku -= np.random.random((1250,1250,3))*np.sign(sudoku-0.5)*0.4
    return sudoku,digits

if __name__ == "__main__":
    sudoku = 
