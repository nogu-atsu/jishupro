import numpy as np
import matplotlib.pyplot as plt
import cv2
from classifier2 import CNN

images = np.load("images.npy")
images_th = [cv2.adaptiveThreshold(images[i].astype(np.uint8),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,5) for i in range(120)]
join_img = images[0]
overlap = np.ones((len(join_img),1),dtype=np.int32)
for i in range(1,120):
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
sum0 = np.sum(sudoku,axis=0)/255.
sum1 = np.sum(sudoku[3:,:],axis=1)/255.
thres0 = (np.max(sum0)+np.min(sum0))/2
thres1 = (np.max(sum1)+np.min(sum1))/2
s0 = np.where(sum0<thres0)[0]
s1 = np.where(sum1<thres1)[0]
sudoku = sudoku[s1[0]:s1[-1],s0[0]+3:s0[-1]+3]
plt.imshow(sudoku,"gray")
plt.show()
sudoku = np.rot90(cv2.resize(sudoku,(32*9,32*9)),3)
sudoku = np.array([sudoku[i//9*32:i//9*32+32,i%9*32:i%9*32+32] for i in range(81)])
"""
for i in range(81):
    plt.subplot(9,9,i+1)
    plt.imshow(sudoku[i],"gray")
    plt.axis("off")
plt.show()
"""
#plt.imshow(sudoku,"gray")
#plt.show()

cnn = CNN()

sudoku = sudoku.reshape(81,32,32,1)
digits = cnn(sudoku).reshape(9,9)
#digits = (digits+1)%10
print(digits)
    
