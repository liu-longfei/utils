import os
import cv2
headstr = """\
<annotation>
    <folder>VOC</folder>
    <filename>NULL</filename>
    <source>
        <database>My Database</database>
        <annotation>COCO</annotation>
        <image>flickr</image>
        <flickrid>NULL</flickrid>
    </source>
    <owner>
        <flickrid>NULL</flickrid>
        <name>company</name>
    </owner>
    <size>
        <width>%d</width>
        <height>%d</height>
        <depth>%d</depth>
    </size>
    <segmented>0</segmented>
"""

objstr = """\
    <object>
        <name>vessel</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
"""

tailstr = """\
</annotation>
"""

# with open('1.txt', 'w') as f:
#     f.write(headstr % ('q', 1, 2, 3))
#     f.write(tailstr)

images_path = r"D:\coder\object_detection\image_ting\one\images"
txt_path = r"D:\coder\object_detection\image_ting\one\trainval1.txt"
save_path = r"D:\coder\object_detection\image_ting\one\test_xml"

for i in open(txt_path).readlines():
    list_1 = i.strip().split(' ')
    print(list_1)  # ['images\\renminyiyuan_LUp_86.jpg', '220,490,268,518,0', '237,349,277,373,0', '269,394,295,415,0']
    list_save = []
    for index, j in enumerate(list_1):
        if index == 0:
            _, img_name = j.split(os.sep)
            xml_name = img_name.split('.')[0] + '.xml'
            print(xml_name)
            img_path = os.path.join(images_path, img_name)
            img = cv2.imread(img_path)  # "D:\coder\object_detection\image_ting\one\images\renminyiyuan_LUp_86.jpg"
            height = img.shape[0]
            width = img.shape[1]
            depth = img.shape[2]
            list_save.append([xml_name, width, height, depth])
        else:
            ymin, xmin, ymax, xmax = int(j.split(',')[0]), int(j.split(',')[1]), int(j.split(',')[2]), int(j.split(',')[3])
            list_save.append([xmin, ymin, xmax, ymax])
    print(list_save)
    for index, val in enumerate(list_save):
        if index == 0:
            with open(os.path.join(save_path, list_save[index][0]), 'a') as f:
                f.write(headstr % (list_save[index][1], list_save[index][2], list_save[index][3]))
                # print('hello')
        else:
            with open(os.path.join(save_path, list_save[0][0]), 'a') as f:
                f.write(objstr % (list_save[index][0], list_save[index][1], list_save[index][2], list_save[index][3]))
                # print('hello')
    else:
        with open(os.path.join(save_path, list_save[0][0]), 'a') as f:
            f.write(tailstr)