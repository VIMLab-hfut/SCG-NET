# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import os
import random
#####划分训练和测试集
train_percent= 0.7  #可自行进行调节
xmlfilepath ='E:/Project/yolov5_small/cloth_detection/annotations'
txtsavepath = 'E:/Project/yolov5_small/cloth_detection/Main'

os.makedirs(txtsavepath,exist_ok=True)
total_xml = os.listdir(xmlfilepath)

num = len(total_xml)
print('xml_num:',num)

list = range(num)
tr = int(num * train_percent)
train = random.sample(list, tr)
ftest = open('E:/Project/yolov5_small/cloth_detection/Main/test.txt', 'w')
ftrain = open('E:/Project/yolov5_small/cloth_detection/Main/train.txt', 'w')
for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in train:
        ftrain.write(name)
    else:
        ftest.write(name)
ftrain.close()
ftest.close()
