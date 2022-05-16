import sys
import os
import cv2
import numpy as np
import os.path
from PIL import Image
from xml.dom.minidom import Document
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
#from sklearn import datasets
from sklearn.datasets import load_iris

def read_xml_annotation(root, image_id):
    in_file = open(os.path.join(root, image_id))
    tree = ET.parse(in_file)
    root = tree.getroot()
    bndboxlist = []

    for object in root.findall('object'):  # 找到root节点下的所有country节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        xmin = int(bndbox.find('xmin').text)
        xmax = int(bndbox.find('xmax').text)
        ymin = int(bndbox.find('ymin').text)
        ymax = int(bndbox.find('ymax').text)
        # print(xmin,ymin,xmax,ymax)
        bndboxlist.append([xmin, ymin, xmax, ymax])
        # print(bndboxlist)

    bndbox = root.find('object').find('bndbox')
    return bndboxlist

def trans(m):
    for i in range(len(m)):
        for j in range(i):
            m[i][j], m[j][i] = m[j][i], m[i][j]
    return m

if __name__ == "__main__":

   XML_DIR = "E:/Project/yolov5_small/cloth_detection0109/annotations"
   #directory = "E:/2"
   # bndbox = []
   length = []
   width = []
   area = []
   ratio = []
   for root, sub_folders, files in os.walk(XML_DIR):
       for name in files:
           file_name = os.path.splitext(name)[0]
           file_houzui = os.path.splitext(name)[1]
           if file_houzui == '.xml':
               bndbox = read_xml_annotation(XML_DIR, name)
               # print(len(bndbox))
               for i in range(len(bndbox)):
                 # length = bndbox[i][2] - bndbox[i][0]
                 # width = bndbox[i][3] - bndbox[i][1]
                 length.append(bndbox[i][2] - bndbox[i][0])
                 width.append(bndbox[i][3] - bndbox[i][1])
                 area.append(length[i] * width[i])
                 ratio.append(length[i] / width[i])
   length= np.array(length)
   length = length.reshape(length.shape[0], 1)
   # print(length)
   width = np.array(width)
   width = width.reshape(width.shape[0], 1)
   area = np.array(area)
   area = area.reshape(area.shape[0], 1)
   print(area)
   ratio = np.array(ratio)
   ratio = ratio.reshape(ratio.shape[0], 1)
   print(ratio)
   anchor = np.hstack((ratio, length))
   # print(anchor)
   print(i)
   #kmeans聚类 
   estimator = KMeans(n_clusters=3)  # 构造聚类器
   estimator.fit(ratio)  # 聚类
   label_pred = estimator.labels_  # 获取聚类标签

   fig = plt.figure()
   ax1 = fig.add_subplot(2, 1, 1)  # 画2行1列个图形的第1个
   ax2 = fig.add_subplot(2, 1, 2)  # 画2行1列个图形的第2个

   # 绘制数据分布图
   ax1.scatter(anchor[:, 0], anchor[:, 1], c="red", marker='o', label='see')
   ax1.set_xlabel('ratio')
   ax1.set_ylabel('area')
   plt.legend(loc=2)
   # 绘制k-means结果
   x0 = anchor[label_pred == 0]
   x1 = anchor[label_pred == 1]
   x2 = anchor[label_pred == 2]
   # x3 = anchor[label_pred == 3]
   ax2.scatter(x0[:, 0], x0[:, 1], c="red", marker='o')
   ax2.scatter(x1[:, 0], x1[:, 1], c="green", marker='*')
   ax2.scatter(x2[:, 0], x2[:, 1], c="blue", marker='+')
   # ax2.scatter(x3[:, 0], x3[:, 1], c="cyan", marker='.', label='Large')
   ax2.set_xlabel('ratio')
   ax2.set_ylabel('length')
   plt.legend(loc=2)
   plt.show()

