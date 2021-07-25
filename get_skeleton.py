from skimage.morphology import skeletonize
from skimage import data
import sknw
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import csv

# 读取图像
#img = data.horse()
img = Image.open('.\\results\\result.jpg')
#img = img.resize((512, 256),Image.ANTIALIAS)

img = np.array(img)
a = []
for i in range(len(img)):
    b = []
    for j in range(len(img[i])):
        if img[i][j][0]*0.299+img[i][j][1]*0.587+img[i][j][2]*0.114>255*0.75:
            b.append(True)
        else:
            b.append(False)
    a.append(b)
img = np.array(a)

# 骨架提取
ske = skeletonize(~img).astype(np.uint16)

# 矢量化调用函数
graph = sknw.build_sknw(ske)

#add
def join_nodes(graph):
    node, nodes = graph._node, graph.nodes()
    center_node = np.array([node[i]['o'] for i in nodes])
    all_nodes = np.array([node[i]['pts'] for i in nodes])
    for (s, e) in graph.edges():
        ps = graph[s][e]['pts']
        s_center_node = center_node[s]
        e_center_node = center_node[e]
        s_all_nodes = all_nodes[s]
        e_all_nodes = all_nodes[e]
        s_line_point = ps[0]
        e_line_point = ps[-1]
        #线长度为一的不进行扩展，以免后续清洗不掉
        if len(ps)==1:
            continue
        if len(s_all_nodes)==1:
            graph[s][e]['pts'] = np.vstack((s_center_node,graph[s][e]['pts']))
        else:
            bbox = [min(s_center_node[0],s_line_point[0]),max(s_center_node[0],s_line_point[0]),
                    min(s_center_node[1],s_line_point[1]),max(s_center_node[1],s_line_point[1])]
            s_crop_nodes = [i for i in s_all_nodes if i[0]>=bbox[0] and i[0]<=bbox[1] and i[1]>=bbox[2] and i[1]<=bbox[3]][::-1]
            for i in s_crop_nodes:
                graph[s][e]['pts'] = np.vstack((np.array(i),graph[s][e]['pts']))
 
        if len(e_all_nodes)==1:
            graph[s][e]['pts'] = np.vstack((graph[s][e]['pts'],e_center_node))
        else:
            bbox = [min(e_center_node[0],e_line_point[0]),max(e_center_node[0],e_line_point[0]),
                    min(e_center_node[1],e_line_point[1]),max(e_center_node[1],e_line_point[1]),]
            e_crop_nodes = [i for i in e_all_nodes if i[0]>=bbox[0] and i[0]<=bbox[1] and i[1]>=bbox[2] and i[1]<=bbox[3]][::-1]
            for i in e_crop_nodes:
                graph[s][e]['pts'] = np.vstack((graph[s][e]['pts'],np.array(i)))
    return graph

#连接节点
graph = join_nodes(graph)

"""
# draw image
plt.imshow(img, cmap='gray')

# draw edges by pts
for (s, e) in graph.edges():
    ps = graph[s][e]['pts']
    plt.plot(ps[:, 1], ps[:, 0], 'green')

# draw node by o
# node, nodes = graph._node, graph.nodes()
# ps = np.array([node[i]['o'] for i in nodes])
# plt.plot(ps[:, 1], ps[:, 0], 'r.')


# title and show
plt.title('Build Graph')
plt.show()
# plt.savefig('pc.png')
"""

output = []
for (s, e) in graph.edges():
    ps = graph[s][e]['pts']
    output.append(ps)
with open('.\\results\\result.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(output)