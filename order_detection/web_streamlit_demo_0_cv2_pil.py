import cv2
import json
import math
import numpy as np
import streamlit as st

from loguru import logger
from ultralytics import YOLO
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont


# 使用yolo检测图片中的信息
def detection_img(img, model):
    model = YOLO(model)

    results = model(img)
    # results[0].save(filename=img.replace('.png', '_results_t.png'))
    return results[0].to_json()


# OCR提取订单编号
def extract_order_number(img, detection_res):
    try:
        detection_res_json = json.loads(detection_res)
        # 提取订单编号的区域
        order_number_area = [i.get('box', {}) for i in detection_res_json if i.get('name', {}) == 'order_number']
        x1, y1 = int(order_number_area[0]['x1']), int(order_number_area[0]['y1'])
        x2, y2 = math.ceil(order_number_area[0]['x2']), math.ceil(order_number_area[0]['y2'])
        # img = cv2.imread(img)
        img = np.array(img)
        crop_img = img[y1: y2, x1: x2]

        ocr = PaddleOCR(use_angle_cls=True, lang='ch')
        ocr_result = ocr.ocr(crop_img, cls=True)
        order_number = ocr_result[0][1][1][0]
        logger.info(f"提取到订单号：{order_number}")

    except Exception as e:
        logger.error(f'提取订单编号报错:{e}')
    return order_number


# 将信息写入图片中
def draw_img_text(img, order_number, detection_res):
    try:
        detection_res_json = json.loads(detection_res)
        # 提取买方的右上角位置
        order_number_area = [i.get('box', {}) for i in detection_res_json if i.get('name', {}) == 'buyer']
        x2, y1 = math.ceil(order_number_area[0]['x2']), int(order_number_area[0]['y1'])
        img_array = np.array(img)
        # 获取字体的高度
        text, font, font_scale, thickness = order_number,cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
        img_text_list = ['超聚变合同号：' + order_number, "腾讯TSPO号：TSPO11111111", "2250TX V7 3台",
                         "交付项目经理：李鹏 00010467", "说明：腾讯系统一TSPO号为维度整单验收，TSPO号和超聚变合同号一一对应关系。"]
        # opencv不支持汉字,使用Pillow库
        # img = get_img_multi_lines_text_cv2(img, img_text_list, (x2, y1), font, font_scale, thickness)
        img = get_img_multi_lines_text_PIL(img_array, img_text_list, (x2, y1), 16)
        logger.info('将信息写入图片成功')
    except Exception as e:
        logger.error(f'将信息写入图片报错：{e}')
    return img


# 根据文字列表，拼接成多行写到图片中,opencv的putText不支持中文
def get_img_multi_lines_text_cv2(img, text_list, pos, font, font_scale=1, thickness=1):
    if len(text_list) == 0:
        return img
    for idx, val in enumerate(text_list):
        y_pos = pos[1]
        if idx == 0:
            cv2.putText(img, text_list[idx], (pos[0], pos[1]), font, font_scale, (0, 0, 255), thickness)
        else:
            (_, text_height), _ = cv2.getTextSize(text_list[idx-1], font, font_scale, thickness)
            y_pos += text_height + 3
            cv2.putText(img, text_list[idx], (pos[0], y_pos), font, font_scale, (0, 0, 255), thickness)
    return img


#  根据文字列表，拼接成多行写到图片中,PIL库支持中文
def get_img_multi_lines_text_PIL(img, text_list, pos, font_size, font_path=r'D:\data\code\order_detection\simfang.ttf'):
    try:
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        font = ImageFont.truetype(font_path, font_size)
        for i, line in enumerate(text_list):
            draw.text((pos[0], pos[1] + i * font_size), line, font=font, fill=(255, 0, 0))
        img_with_text = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        logger.info('将订单信息写入图片成功')
    except Exception as e:
        logger.error(f'订单信息写入图片报错：{e}')
    return img_with_text


# 框出状态和验收完成日期
def draw_box_status_finish_data(img, detection_res):
    try:
        detection_res_json = json.loads(detection_res)
        # 获取状态位置信息
        status_area = [i.get('box', {}) for i in detection_res_json if i.get('name', {}) == 'status']
        status_x1, status_y1 = int(status_area[0]['x1']), int(status_area[0]['y1'])
        status_x2, status_y2 = math.ceil(status_area[0]['x2']), math.ceil(status_area[0]['y2'])
        cv2.rectangle(img, (status_x1, status_y1), (status_x2, status_y2), (0, 0, 255), 1)
        # 获取验收完成日期的位置信息
        finish_data_area = [i.get('box', {}) for i in detection_res_json if i.get('name', {}) == 'finish_data']
        finish_data_area_x1, finish_data_area_y1 = int(finish_data_area[0]['x1']), int(finish_data_area[0]['y1'])
        finish_data_area_x2, finish_data_area_y2 = math.ceil(finish_data_area[0]['x2']), math.ceil(finish_data_area[0]['y2'])
        cv2.rectangle(img, (finish_data_area_x1, finish_data_area_y1), (finish_data_area_x2, finish_data_area_y2), (0, 0, 255), 1)
        # cv2.imshow('img', img)
        # cv2.waitKey(0)
        logger.info('框出状态和验收完成日期成功')
    except Exception as e:
        logger.error(f'框出状态和验收完成日期报错：{e}')
    return img


# 拼接图片名称
def concate_img_name():
    return '测试demo.png'


# 根据订单信息获取合同详细信息
def get_contract_info(order_number):
    pass


if __name__ == '__main__':
    detection_model = r'D:\data\code\order_detection\runs\detect\train\weights\best.pt'
    img_path = r'D:\data\code\order_detection\image.png'
    # 设置页面标题
    st.title("图片处理应用")

    # 上传图片
    uploaded_file = st.file_uploader("上传一张图片", type=["jpg", "jpeg", "png"])


    if uploaded_file is not None:
        # 读取上传的图片
        image = Image.open(uploaded_file)

        # 使用yolo检测图片中的信息
        detection_res = detection_img(image, detection_model)

        # OCR提取订单编号
        order_number = extract_order_number(image, detection_res)

        # 将信息写入图片中
        img_text = draw_img_text(image, order_number, detection_res)

        img = draw_box_status_finish_data(img_text, detection_res)

        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        save_img = concate_img_name()
        img.save(save_img)

        # 显示修改后的图片
        st.image(img, caption="修改后的图片", use_container_width=True)

        # 提供下载链接
        with open(save_img, "rb") as f:
            st.download_button("下载", f, file_name=save_img)
