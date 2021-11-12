import os
import shutil
import cv2

# txt_path = r"D:\coder\object_detection\trainval1.txt"


txt_path = r"D:\coder\object_detection\test.txt"  # yolov4的txt文件
img_root = r"D:\coder\object_detection\images"  # yolov4的图片路径
# train_save_root = r"D:\coder\object_detection\my_yolo_dataset\train\images"
# val_save_root = r"D:\coder\object_detection\my_yolo_dataset\train\labels"
train_save_root = r"D:\coder\object_detection\my_yolo_dataset\val\images"  # 将要存放的图片路径
val_save_root = r"D:\coder\object_detection\my_yolo_dataset\val\labels"  #  存放yolov3的txt路径

for i in open(txt_path, 'r').readlines():
    list_1 = i.strip().split(' ')
    print(list_1)
    for index, val in enumerate(list_1):
        if index == 0:
            img_name = val.split(os.sep)[-1]
            img_path = os.path.join(img_root, img_name)
            img_shape = cv2.imread(img_path)
            img_height = img_shape.shape[0]
            img_width = img_shape.shape[1]
            shutil.copy(img_path, train_save_root)
        else:
            xmin, ymin, xmax, ymax = float(val.split(',')[1]), float(val.split(',')[0]), float(val.split(',')[3]), float(val.split(',')[2])
            xcenter = xmin + (xmax - xmin) / 2
            ycenter = ymin + (ymax - ymin) / 2
            w = xmax - xmin
            h = ymax - ymin
            xcenter = round(xcenter / img_width, 6)
            ycenter = round(ycenter / img_height, 6)
            w = round(w / img_width, 6)
            h = round(h / img_height, 6)

            if xcenter < 0 or ycenter < 0 or w < 0 or h < 0 or xcenter > 1 or ycenter > 1 or w > 1 or h > 1:
                continue

            info = [str(i) for i in [0, xcenter, ycenter, w, h]]

            with open(os.path.join(val_save_root, list_1[0].split(os.sep)[-1].split('.')[0] + '.txt'), 'a') as f:
                f.write(" ".join(info) + '\n')

