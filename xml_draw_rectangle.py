import os

import cv2
import xml.etree.ElementTree as ET

image_dir = r"D:\coder\object_detection\my_datas\images"   # 将要画框的图片
rectangle_image_path = r"D:\coder\object_detection\my_datas\images_rectangle"  # 画框图片的存放目录
xml_path = r"D:\coder\object_detection\my_datas\images_xml"

image_list = os.listdir(image_dir)
xml_list = os.listdir(xml_path)

assert len(image_list) == len(xml_list), "len(image_list) != len(xml_list)"

for index in range(len(image_list)):
    image_dir = r"D:\coder\object_detection\my_datas\images"
    image_path = os.path.join(image_dir, image_list[index])
    xml_path = r"D:\coder\object_detection\my_datas\images_xml"
    xml_path = os.path.join(xml_path, xml_list[index])
    print(xml_path)
    read_xml = open(xml_path)
    tree = ET.parse(read_xml)
    root = tree.getroot()
    img = cv2.imread(image_path)
    for obj in root.iter('object'):
        xml_box = obj.find('bndbox')
        x_min, y_min, x_max, y_max = int(xml_box.find('xmin').text), int(xml_box.find('ymin').text), int(xml_box.find('xmax').text), int(xml_box.find('ymax').text)
        print(x_min, y_min, x_max, y_max)
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    cv2.imwrite(os.path.join(rectangle_image_path, image_list[index]), img)