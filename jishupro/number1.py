#python3用
import tensorflow as tf
import numpy as np
from recog_sudoku3 import Recog_Sudoku
import time
import matplotlib.pyplot as plt

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

x = tf.placeholder(tf.float32,shape=[None,32,32,1])
t = tf.placeholder(tf.float32,shape=[None,10])
w_conv1 = tf.Variable(tf.truncated_normal([5,5,1,32], stddev=0.1))
b_conv1 = tf.Variable(tf.truncated_normal([32], stddev=0.1))
h_conv1 = tf.nn.relu(conv2d(x, w_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)
w_conv2 = tf.Variable(tf.truncated_normal([5,5,32,64], stddev=0.1))
b_conv2 = tf.Variable(tf.truncated_normal([64], stddev=0.1))
h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)
w_fc1 = tf.Variable(tf.truncated_normal([8*8*64,1024], stddev=0.1))
b_fc1 = tf.Variable(tf.truncated_normal([1024], stddev=0.1))
h_pool2_flat = tf.reshape(h_pool2, [-1, 8*8*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)
w_fc2 = tf.Variable(tf.truncated_normal([1024,10], stddev=0.1))
b_fc2 = tf.Variable(tf.truncated_normal([10], stddev=0.1))
y_conv = tf.matmul(h_fc1, w_fc2) + b_fc2

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_conv, t))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(t,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess = tf.InteractiveSession()
sess.run(tf.initialize_all_variables())
filename = "number1.ckpt"
saver = tf.train.Saver()
saver.restore(sess,filename+"-7000")
"""
test_x = []
test_y = []
for i in range(10):
    _x,_,_y=Recog_Sudoku()
    test_x.extend(_x)
    test_y.extend(_y)
test_x = np.array(test_x,dtype=np.float32).reshape(-1,16,16,1)
test_y = np.eye(9)[np.array(test_y).reshape(-1)-1]
"""
"""
#学習
accu=0
for i in range(20000):
    time1 = time.time()
    train_x,_,train_y=Recog_Sudoku()
    time2 = time.time()
    train_x = train_x.reshape(-1,32,32,1)
    train_y = np.eye(10)[train_y.reshape(-1)-1]
    dict = {x:train_x,t:train_y}
    if i%10 == 0:
        train_accuracy = accuracy.eval(feed_dict = dict)
        accu=accu*0.95+train_accuracy*0.05
        print("step %d, training accuracy %g time %f"%(i, accu,time2-time1))
    if i%1000==0:
        saver.save(sess,filename,global_step=i)
    train_step.run(feed_dict=dict)

#print("test accuracy %g"%accuracy.eval(feed_dict={x:test_x,t:test_y}))
#学習終わり
"""
sample_x = np.zeros((1,32,32,1))
sample_y = np.zeros((1,10))
weights = np.array(sess.run([w_conv1,b_conv1,w_conv2,b_conv2,w_fc1,b_fc1,w_fc2,b_fc2],feed_dict = {x:sample_x,t:sample_y}))
np.save("weights.npy",weights)


