import csv
import os
import numpy as np
import random

data = []
with open("data.csv", 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        temp = np.array(row).astype(np.float).tolist()
        data.append(temp)
        
minobj = 9999999999999999
maxobj = -9999999999999999
for i in range(len(data)):
    if data[i][len(data[i])-1]>maxobj:
        maxobj = data[i][len(data[i])-1]
    if data[i][len(data[i])-1]<minobj:
        minobj = data[i][len(data[i])-1]      

minobj = minobj - (maxobj-minobj)*0.25
maxobj = maxobj + (maxobj-minobj)*0.25

for i in range(len(data)):
    data[i][len(data[i])-1] = (data[i][len(data[i])-1]-minobj)/(maxobj-minobj)

num = len(data[0])-1

import tensorflow.compat.v1 as tf
tf.disable_eager_execution()

def initialize():
    #placeholder
    x = tf.placeholder(tf.float32, [None, D_in])
    y = tf.placeholder(tf.float32, [None, D_out])
    w = {
        'h1': tf.Variable(tf.random_normal([D_in, D_h1])),
        'h2': tf.Variable(tf.random_normal([D_h1, D_h2])),
        #'h3': tf.Variable(tf.random_normal([D_h2, D_h3])),
        #'h4': tf.Variable(tf.random_normal([D_h3, D_h4])),
        #'h5': tf.Variable(tf.random_normal([D_h4, D_h5])),
        #'h6': tf.Variable(tf.random_normal([D_h5, D_h6])),
        'out': tf.Variable(tf.random_normal([D_h2, D_out]))
    }
    b = {
        'h1': tf.Variable(tf.random_normal([D_h1])),
        'h2': tf.Variable(tf.random_normal([D_h2])),
        #'h3': tf.Variable(tf.random_normal([D_h3])),
        #'h4': tf.Variable(tf.random_normal([D_h4])),
        #'h5': tf.Variable(tf.random_normal([D_h5])),
        #'h6': tf.Variable(tf.random_normal([D_h6])),
        'out': tf.Variable(tf.random_normal([D_out]))
    }

    #activation functions #tf.layers.batch_normalization()
    def multilayer_perceptron(x):
        h1_layer = tf.sigmoid(tf.add(tf.matmul(x, w['h1']), b['h1']))
        h2_layer = tf.sigmoid(tf.add(tf.matmul(h1_layer, w['h2']), b['h2']))
        #h3_layer = tf.sigmoid(tf.add(tf.matmul(h2_layer, w['h3']), b['h3']))
        #h4_layer = tf.sigmoid(tf.add(tf.matmul(h3_layer, w['h4']), b['h4']))
        #h5_layer = tf.sigmoid(tf.add(tf.matmul(h4_layer, w['h5']), b['h5']))
        #h6_layer = tf.sigmoid(tf.add(tf.matmul(h5_layer, w['h6']), b['h6']))
        out_layer = tf.sigmoid(tf.add(tf.matmul(h2_layer, w['out']), b['out']))
        return out_layer
    pred = multilayer_perceptron(x)

    #loss function
    #cost = tf.reduce_sum(tf.where(tf.greater(pred, 0.932), 10*(y-pred)*(y-pred),
    #                     tf.where(tf.greater(0.042, pred), 10*(y-pred)*(y-pred),
    #                     (y-pred)*(y-pred))))
    cost = tf.reduce_sum((y-pred)*(y-pred))

    #optimizer and others
    optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)
    init = tf.global_variables_initializer()
    variables_dict = {
        'b1': b['h1'],
        'b2': b['h2'],
        #'b3': b['h3'],
        #'b4': b['h4'],
        #'b5': b['h5'],
        #'b6': b['h6'],
        'bout': b['out'],
        'w1': w['h1'],
        'w2': w['h2'],
        #'w3': w['h3'],
        #'w4': w['h4'],
        #'w5': w['h5'],
        #'w6': w['h6'],
        'wout': w['out']
    }
    saver = tf.train.Saver(variables_dict)
    saver = tf.train.Saver(max_to_keep=1000, keep_checkpoint_every_n_hours=1)
    return x, y, pred, cost, optimizer, init, saver
        
        
def evaluatewhentrain(xdata, modelfile):
    with tf.Session() as sess:
        saver.restore(sess, modelfile)
        yhat = pred.eval(feed_dict = {x: xdata})
    return yhat


def train(X_test, y_test):
    with tf.Session() as sess:
        sess.run(init)
        merged_all = tf.summary.merge_all()
        writer = tf.summary.FileWriter('logs/', sess.graph)
        for epoch in range(training_epochs):
            avg_cost = 0.
            total_batch = int(num/batch_size)
            if num%batch_size != 0:
                total_batch = total_batch + 1
            for i in range(total_batch):
                batch_xs = xdata[i*batch_size:(i+1)*batch_size]
                batch_ys = ydata[i*batch_size:(i+1)*batch_size]
                _, c = sess.run([optimizer, cost], feed_dict={x: batch_xs, y: batch_ys})
                avg_cost += c / total_batch
            if (epoch+1) % display_step == 0 or epoch == 0:
                print("Epoch:", '%04d' % (epoch+1), " cost=", "{:.9f}".format(avg_cost))
                #merged = sess.run(merged_all, feed_dict={x: batch_xs, y: batch_ys})
                #writer.add_summary(merged, epoch)
            if (epoch+1) % save_step == 0:
                saver.save(sess, "./model/model"+str(epoch)+".ckpt")
                print("save model done.")
                yhat = np.array(evaluatewhentrain(X_test,"./model/model"+str(epoch)+".ckpt"))
                accuracy = 100 - np.around(np.median(np.abs(yhat-y_test)/yhat*100,axis=0),decimals=1)
                print('5-layer ANN', accuracy, '% Step '+str(epoch))

#training settings
training_epochs = 1000
save_step = 100

batch_size = min(len(data),10)
display_step = 10

#network structure
D_in, D_out = num, 1
D_h1 = int((num+1)/4)+1
D_h2 = int((num+1)/16)+1
#D_h3 = int((num+1)/8)+1
#D_h4 = int((num+1)/16)+1
#D_h5 = 20
#D_h6 = 20

#initialize
x, y, pred, cost, optimizer, init, saver = initialize()

#load data
xdata = np.array(data)[:,0:num]
ydata = np.mat(np.array(data)[:,num]).T
X_test = np.array(data)[:,0:num]
y_test = np.mat(np.array(data)[:,num]).T

train(X_test, y_test)