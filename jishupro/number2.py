#python3用
import tensorflow as tf
import numpy as np
import time
import matplotlib.pyplot as plt
import cv2

def make_data():
    ims = np.load("number_images.npy")
    digits = np.random.randint(0,10,size=[9,9])
    sudoku = np.load("waku.npy")
    
    for i in range(9):
        for j in range(9):
            if digits[i][j]!=0:
                sudoku[860+i*410-len(ims[digits[i][j]-1])//2:860+i*410+len(ims[digits[i][j]-1])-len(ims[digits[i][j]-1])//2,860+j*410-len(ims[digits[i][j]-1][0])//2:860+j*410+len(ims[digits[i][j]-1][0])-len(ims[digits[i][j]-1][0])//2,:]=ims[digits[i][j]-1]/255

    sudoku = cv2.resize(sudoku,(500,500))[:,:,0]
    sudoku=sudoku*0.9+0.05
    sudoku+=np.random.uniform(-0.05,0.05,[500,500])
    sudoku = (sudoku*255).astype(np.uint8)
    points1 = np.array([[0,0],[0,500],[500,0],[500,500]],dtype=np.float32)
    points2 = points1+np.random.randint(0,5,[4,2]).astype(np.float32)*(-np.sign(points1-200))
    pers = cv2.getPerspectiveTransform(points2,points1);
    sudoku = cv2.warpPerspective(sudoku, pers, (500,500));
    sum0 = np.sum(sudoku,axis=0)/255.
    sum1 = np.sum(sudoku,axis=1)/255.
    thres0 = (np.max(sum0)+np.min(sum0))/2
    thres1 = (np.max(sum1)+np.min(sum1))/2
    s0 = np.where(sum0<thres0)[0]
    s1 = np.where(sum1<thres1)[0]
    sudoku = sudoku[s1[0]:s1[-1],s0[0]:s0[-1]]
    sudoku = cv2.resize(sudoku,(32*9,32*9))
    sudoku = cv2.adaptiveThreshold(sudoku,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,5)
    sudoku = np.array([sudoku[i//9*32:i//9*32+32,i%9*32:i%9*32+32] for i in range(81)])
    """
    for i in range(81):
        plt.subplot(9,9,i+1)
        plt.imshow(sudoku[i],"gray")
        plt.axis("off")
    plt.show()
    """
    return sudoku,digits

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
filename = "number2-1.ckpt"
saver = tf.train.Saver()
restore_step = 6000
saver.restore(sess,filename+"-"+str(restore_step))

#学習
accu=0
for i in range(20000):
    time1 = time.time()
    train_x,train_y=make_data()
    time2 = time.time()
    train_x = train_x.reshape(-1,32,32,1)
    train_y = np.eye(10)[train_y.reshape(-1)]
    dict = {x:train_x,t:train_y}
    train_step.run(feed_dict=dict)
    _,train_accuracy,loss = sess.run([train_step,accuracy,cross_entropy],feed_dict = dict)
    train_accuracy = accuracy.eval(feed_dict = dict)
    accu+=train_accuracy
    if i%10==0:
        print("step %d, training accuracy %g time %f"%(i,accu/(i+1),time2-time1))
    if i%1000==0:
        saver.save(sess,filename,global_step=i+restore_step)
        sample_x = np.zeros((1,32,32,1))
        sample_y = np.zeros((1,10))
        weights = np.array(sess.run([w_conv1,b_conv1,w_conv2,b_conv2,w_fc1,b_fc1,w_fc2,b_fc2],feed_dict = {x:sample_x,t:sample_y}))
        np.save("weights2-1"+str(i+restore_step)+".npy",weights)

#print("test accuracy %g"%accuracy.eval(feed_dict={x:test_x,t:test_y}))
#学習終わり
