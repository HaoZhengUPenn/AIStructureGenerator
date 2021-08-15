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


def annealing(steps,n,goal):
    state = start_state(n)
    T = 1
    cost = f_annealing(state,goal)
    states, costs = [state], [cost]
    for step in range(steps):
        T = temperature(T)
        new_state = random_neighbour(state, T, n)
        new_cost = f_annealing(new_state,goal)
        if acceptance_probability(cost, new_cost, T) > rn.random():
            state, cost = new_state, new_cost
            states.append(state)
            costs.append(new_cost)
        if (step+1)%display_step==0:
            print("SA step "+str(step)+" cost = "+str(cost))
    return state, cost, states, costs

def f_annealing(state,goal):
    npstate = np.array(state).reshape((1, num))
    yhat = pred.eval(feed_dict = {x: npstate})
    new_goal = yhat
    return abs(goal-new_goal)

def start_state(n):
    """ 0.5 point in the interval."""
    return [0.5 for i in range(n)]

def random_neighbour(state, T, n):
    """Move a little bit x, from the left or the right."""
    rec = []
    for i in range(n):
        u = rn.random_sample()
        if u>0.5:
            y = T * ((1 + 1/T)**abs(2*u - 1) - 1.0)
        else:
            y = - T * ((1 + 1/T)**abs(2*u - 1) - 1.0)
        delta = (1 - 0) * y
        rec.append(clip(state[i] + delta))
    return rec

def acceptance_probability(cost, new_cost, temperature):
    if new_cost < cost:
        return 1
    else:
        p = np.exp(- (new_cost - cost) / temperature)
        return p

def temperature(T):
    """ Example of temperature dicreasing as the process goes on."""
    return T*0.975

def clip(x):
    """ Force x to be in the interval."""
    a, b = 0, 1
    return max(min(x, b), a)

import numpy.random as rn
import numpy as np
import csv

data = []
with open("data.csv", 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        temp = np.array(row).astype(np.float).tolist()
        data.append(temp)
num = len(data[0])-1

display_step = 100

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

with tf.Session() as sess:
    saver.restore(sess, "./model/model999.ckpt")
    temp = annealing(10000,num,1)
    goalstate = np.array(temp[0]).reshape((1,num))
    np.savetxt("results.csv", goalstate, delimiter=',')