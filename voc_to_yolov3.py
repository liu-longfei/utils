# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET
import os
import cv2

classes = ["dog", "cat"]   # 自己的类别名称


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id, Image_root):
    # in_file = open('../PrepareImage/anno/%s.xml' % (image_id))   # 标注图片的xml格式存放路径
    in_file = open(r"C:\Users\longfeiliu-n\Desktop\voc_to_yolov3\anno/%s.xml" % (image_id))

    out_file = open(r'C:\Users\longfeiliu-n\Desktop\voc_to_yolov3\txt/%s.txt' % (image_id), 'w')  # 生成的txt文件存放路径
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')  # 根据不同的xml标注习惯修改
    if size:
        w = int(size.find('width').text)
        h = int(size.find('height').text)
    else:
        jpg_img_patch = Image_root + image_id + '.jpg'
        jpg_img = cv2.imread(jpg_img_patch)
        h, w, _ = jpg_img.shape  # cv2读取的图片大小格式是w,h

    for obj in root.iter('object'):
        difficult = obj.find('difficult')
        if difficult:
            difficult = obj.find('difficult').text
        else:
            difficult = 0
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


Image_root = r"C:\Users\longfeiliu-n\Desktop\voc_to_yolov3\images"   # 图片的路径

fileList = os.listdir(Image_root)
for path in fileList:
    image_ids = path.split(".")
    image_id = image_ids[0]
    convert_annotation(image_id, Image_root)
