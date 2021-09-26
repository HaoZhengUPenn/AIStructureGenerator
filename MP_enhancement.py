from skimage import data, segmentation, color
from skimage.future import graph
from matplotlib import pyplot as plt
import skimage.io
from skimage.color import rgb2gray
import sknw
from skimage.feature import canny
from skimage.morphology import skeletonize
import numpy as np
import csv
from skimage.segmentation import watershed, expand_labels
from skimage import feature
from skimage import measure

name = '.\\results\\result_mp.jpg'

img = skimage.io.imread(name)

labels1 = segmentation.slic(img, compactness=100, n_segments=400,
                            start_label=1)
out1 = color.label2rgb(labels1, img, kind='avg', bg_label=0)

g = graph.rag_mean_color(img, labels1, mode='similarity')

labels2 = graph.cut_normalized(labels1, g)

expanded = expand_labels(labels2, distance=10)

out2 = color.label2rgb(expanded, img, kind='avg', bg_label=0)

edge = feature.canny(rgb2gray(out2), sigma=3)

for i in range(len(edge)):
    for j in range(len(edge[i])):
        if edge[i][j]==True:
            img[i][j][0] = 0
            img[i][j][1] = 0
            img[i][j][2] = 255

skimage.io.imsave('.\\results\\result_mp_enhancement.jpg', img)