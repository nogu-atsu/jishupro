#cnn with pyton
#very slow
import numpy as np
from scipy import signal
from recog_sudoku3 import Recog_Sudoku

def conv2d(x,w):
    npad = ((0, 0), (x.shape[1]//2, x.shape[1]//2), (x.shape[2]//2, x.shape[2]//2),(0, 0))
    x_ = np.pad(x, pad_width=npad, mode='constant', constant_values=0)
    return np.transpose(np.array([signal.convolve(x_,w[np.newaxis,::-1,::-1,::-1,i],mode="valid")[:,:,:,0] for i in range(w.shape[3])]),[1,2,3,0])
def max_pool_2x2(x):
    return np.transpose(np.amax(np.transpose(x.reshape(x.shape[0],x.shape[1],-1,2,x.shape[3]),[0,2,1,3,4]).reshape(x.shape[0],x.shape[1]//2,x.shape[2]//2,4,x.shape[3]),axis=3,keepdims=True),[0,2,1,3,4])[:,:,:,0,:]
def relu(x):
    return x*(x>0)

train_x,_,train_y=Recog_Sudoku()
print(1)
train_x = train_x.reshape(-1,32,32,1)
print(2)
train_y = np.eye(10)[train_y.reshape(-1)-1]
print(3)
w_c1,b_c1,w_c2,b_c2,w_f1,b_f1,w_f2,b_f2 = np.load("weights.npy")
print(4)
h_c1 =relu(conv2d(train_x,w_c1)+b_c1)
print(5)
h_p1 =max_pool_2x2(h_c1)
print(6)
h_c2 =relu(conv2d(h_p1,w_c2)+b_c2)
print(7)
h_p2 =max_pool_2x2(h_c2)
print(8)
h_p2_flat =h_p2.reshape(-1,8*8*64)
print(9)
h_f1 =relu(np.dot(h_p2_flat,w_f1)+b_f1)
print(10)
y_conv =np.dot(h_f1,w_f2)+b_f2

print(y_conv.argmax(axis=0))
print(train_y)
