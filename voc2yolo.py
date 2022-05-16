import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets = ['train', 'test']
# classes = ['擦洞','吊经','毛洞','跳花']  #自己训练的类别
classes = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle', 'large-vehicle', 'ship', 'tennis-court','basketball-court', 'storage-tank',
        'soccer-ball-field', 'roundabout', 'harbor', 'swimming-pool', 'helicopter', 'container-crane']  #自己训练的类别
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0-1
    y = (box[2] + box[3]) / 2.0-1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)
root_path='E:/Project/yolov5_small/cloth_detection/'
def convert_annotation(image_id):
    in_file = open(root_path+'annotations/%s.xml' % (image_id))
    print(image_id)
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    # w = int(size.find('width').text)
    # h = int(size.find('height').text)
    # d = int(size.find('depth').text)
    w = 800
    h = 800
    d = 3



    out_file = open(root_path+'labels/%s.txt' % (image_id), 'w')
    for obj in root.iter('object'):
    #    if obj.find('difficult')==None:
    #         print(image_id)
        # difficult = obj.find('difficult').text
        cls = obj.find('name').text
        # if cls not in classes or int(difficult) == 1:
        if cls not in classes :
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
wd = getcwd()
print(wd)
for image_set in sets:
    if not os.path.exists(root_path+'labels'):
        os.makedirs(root_path+'labels')
    image_ids = open(root_path+'Main/%s.txt' % (image_set)).read().strip().split()
#     image_ids = open(root_path+'Main/%s.txt' % (image_set)).read().split('\n')
    print(image_set)
    list_file = open(root_path+'%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        convert_annotation(image_id)
        list_file.write(root_path+'images/%s.png\n' % (image_id))
    list_file.close()
