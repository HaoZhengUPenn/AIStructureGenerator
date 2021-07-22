import tensorflow.compat.v1 as tf
tf.disable_eager_execution()
import csv
import numpy as np
import sys

def initialize():
    #placeholder
    x = tf.placeholder(tf.float32, [None, D_in])
    y = tf.placeholder(tf.float32, [None, D_out])
    w = {
        'h1': tf.Variable(tf.random_normal([D_in, D_h1])),
        'h2': tf.Variable(tf.random_normal([D_h1, D_h2])),
        'h3': tf.Variable(tf.random_normal([D_h2, D_h3])),
        'h4': tf.Variable(tf.random_normal([D_h3, D_h4])),
        #'h5': tf.Variable(tf.random_normal([D_h4, D_h5])),
        #'h6': tf.Variable(tf.random_normal([D_h5, D_h6])),
        'out': tf.Variable(tf.random_normal([D_h4, D_out]))
    }
    b = {
        'h1': tf.Variable(tf.random_normal([D_h1])),
        'h2': tf.Variable(tf.random_normal([D_h2])),
        'h3': tf.Variable(tf.random_normal([D_h3])),
        'h4': tf.Variable(tf.random_normal([D_h4])),
        #'h5': tf.Variable(tf.random_normal([D_h5])),
        #'h6': tf.Variable(tf.random_normal([D_h6])),
        'out': tf.Variable(tf.random_normal([D_out]))
    }

    #activation functions #tf.layers.batch_normalization()
    def multilayer_perceptron(x):
        h1_layer = tf.sigmoid(tf.add(tf.matmul(x, w['h1']), b['h1']))
        h2_layer = tf.sigmoid(tf.add(tf.matmul(h1_layer, w['h2']), b['h2']))
        h3_layer = tf.sigmoid(tf.add(tf.matmul(h2_layer, w['h3']), b['h3']))
        h4_layer = tf.sigmoid(tf.add(tf.matmul(h3_layer, w['h4']), b['h4']))
        #h5_layer = tf.sigmoid(tf.add(tf.matmul(h4_layer, w['h5']), b['h5']))
        #h6_layer = tf.sigmoid(tf.add(tf.matmul(h5_layer, w['h6']), b['h6']))
        out_layer = tf.sigmoid(tf.add(tf.matmul(h4_layer, w['out']), b['out']))
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
        'b3': b['h3'],
        'b4': b['h4'],
        #'b5': b['h5'],
        #'b6': b['h6'],
        'bout': b['out'],
        'w1': w['h1'],
        'w2': w['h2'],
        'w3': w['h3'],
        'w4': w['h4'],
        #'w5': w['h5'],
        #'w6': w['h6'],
        'wout': w['out']
    }
    saver = tf.train.Saver(variables_dict)
    """
    tf.summary.scalar('loss',cost)
    tf.summary.histogram('b1', b['h1'])
    tf.summary.histogram('b2', b['h2'])
    tf.summary.histogram('b3', b['h3'])
    tf.summary.histogram('b4', b['h4'])
    tf.summary.histogram('bout', b['out'])
    tf.summary.histogram('w1', w['h1'])
    tf.summary.histogram('w2', w['h2'])
    tf.summary.histogram('w3', w['h3'])
    tf.summary.histogram('w4', w['h4'])
    tf.summary.histogram('wout', w['out'])
    """
    saver = tf.train.Saver(max_to_keep=1000, keep_checkpoint_every_n_hours=1)
    return x, y, pred, cost, optimizer, init, saver


def evaluate(filename, dimensionx):
    xdata = []
    with open(filename) as f:
        lines = f.readlines()
    temp = []
    for line in lines:
        temp.append(float(line))
        if len(temp)==dimensionx:
            xdata.append(temp)
            temp = []
    
    with tf.Session() as sess:
        saver.restore(sess, "./model.ckpt")
        yhat = pred.eval(feed_dict = {x: xdata})

#network structure
D_in, D_out = 5, 1
D_h1 = 20
D_h2 = 20
D_h3 = 20
D_h4 = 20
#D_h5 = 20
#D_h6 = 20

#initialize
x, y, pred, cost, optimizer, init, saver = initialize()

with open("pre.csv", 'r') as f:
    a = []
    reader = csv.reader(f)
    for row in reader:
        temp = np.array(row).astype(np.float).tolist()
        a.append(temp)
data_pre = a

maxx = 0
maxy = 0
maxf = 0
minx = 99999999
miny = 99999999
minf = 99999999
for j in range(len(data_pre)):
    if data_pre[j][0]>maxx:
        maxx = data_pre[j][0]
    if data_pre[j][0]<minx:
        minx = data_pre[j][0]
    if data_pre[j][2]>maxx:
        maxx = data_pre[j][2]
    if data_pre[j][2]<minx:
        minx = data_pre[j][2]
    if data_pre[j][1]>maxy:
        maxy = data_pre[j][1]
    if data_pre[j][1]<miny:
        miny = data_pre[j][1]
    if data_pre[j][3]>maxy:
        maxy = data_pre[j][3]
    if data_pre[j][3]<miny:
        miny = data_pre[j][3]
    if data_pre[j][4]>maxf:
        maxf = data_pre[j][4]
    if data_pre[j][4]<minf:
        minf = data_pre[j][4]
print(minx,maxx,miny,maxy,minf,maxf)
for j in range(len(data_pre)):
    data_pre[j][0] = (data_pre[j][0]-minx)/(maxx-minx)
    data_pre[j][2] = (data_pre[j][2]-minx)/(maxx-minx)
    data_pre[j][1] = (data_pre[j][1]-miny)/(maxy-miny)
    data_pre[j][3] = (data_pre[j][3]-miny)/(maxy-miny)
    data_pre[j][4] = (data_pre[j][4]-minf)/(maxf-minf)
    if (data_pre[j][0]>1) or (data_pre[j][0]<0) or (data_pre[j][1]>1) or (data_pre[j][1]<0) or (data_pre[j][2]>1) or (data_pre[j][2]<0) or (data_pre[j][3]>1) or (data_pre[j][3]<0) or (data_pre[j][4]>1) or (data_pre[j][4]<0):
        print("error")

X_pre = data_pre
maxl = 1000

with tf.Session() as sess:
    saver.restore(sess, "./"+sys.argv[1]+"/model999.ckpt")
    yhat = pred.eval(feed_dict = {x: X_pre})
np.savetxt('results.csv', yhat*maxl, delimiter = ',')