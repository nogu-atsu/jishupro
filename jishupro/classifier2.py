import tensorflow as tf
import numpy as np
from recog_sudoku3 import Recog_Sudoku
import time

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')
class CNN:
    def __init__(self):
        w_c1,b_c1,w_c2,b_c2,w_f1,b_f1,w_f2,b_f2 = np.load("weights10000.npy")
        self.x = tf.placeholder(tf.float32,shape=[None,32,32,1])
        w_conv1 = tf.Variable(w_c1)
        b_conv1 = tf.Variable(b_c1)
        h_conv1 = tf.nn.relu(conv2d(self.x, w_conv1) + b_conv1)
        h_pool1 = max_pool_2x2(h_conv1)
        w_conv2 = tf.Variable(w_c2)
        b_conv2 = tf.Variable(b_c2)
        h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2) + b_conv2)
        h_pool2 = max_pool_2x2(h_conv2)
        w_fc1 = tf.Variable(w_f1)
        b_fc1 = tf.Variable(b_f1)
        h_pool2_flat = tf.reshape(h_pool2, [-1, 8*8*64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)
        w_fc2 = tf.Variable(w_f2)
        b_fc2 = tf.Variable(b_f2)
        self.y = tf.argmax(tf.matmul(h_fc1, w_fc2) + b_fc2,1)
        self.sess = tf.InteractiveSession()
        self.sess.run(tf.initialize_all_variables())
    def __call__(self,sudoku):#(81,32,32,1)
        return self.sess.run(self.y,feed_dict = {self.x:sudoku})
    

if __name__ == "__main__":
    cnn = CNN()
    #sudoku,_,_ = Recog_Sudoku(mode=1,image="sudoku_gen.jpg")
    #sudoku = sudoku.reshape(81,32,32,1)
    sudoku = np.ones((81,32,32,1),dtype=np.float32)
    digits = cnn(sudoku).reshape(9,9)
    #digits = (digits+1)%10
    print(digits)
    
