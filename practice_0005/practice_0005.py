#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'


"""
iphone 5 的分辨率：1136×640
按x缩小
按y缩小
旋转
旋转后 按x缩小
旋转后 按y缩小
旋转暂不考虑
"""

from PIL import Image
import imghdr
import os


def resize_image(filename, size=(1136, 640)):
    image_name = os.path.split(filename)[1]
    image_name, image_ext = os.path.splitext(image_name)
    try:
        img = Image.open(filename)
        print(img.size)
        fit_size = adjust_size(img.size, size)
        if fit_size:
            temp_name = '{}_{}_{}.{}'.format(image_name, fit_size[0], fit_size[1], image_ext)
            img.resize(fit_size, resample=Image.LANCZOS).save(temp_name)
    except IOError:
        print('{}文件无法打开'.format(filename))


def adjust_size(s_size, t_size):
    """
    计算图片适配到目标分辨率后的图片大小
    :param s_size: 原图片大小
    :param t_size: 目标分辨率
    :return: 适配后图片大小，tuple
    """
    diff_x, diff_y = s_size[0]-t_size[0], s_size[1]-t_size[1]
    if diff_x > diff_y and diff_x > 0:  # 水平方向直接缩放至目标分辨率的水平大小
        scale = 1 - diff_x/s_size[0]  # 计算垂直方向的缩放比例
        return t_size[0], int(s_size[1]*scale)
    elif diff_y > diff_x and diff_y > 0:  # 垂直方向直接缩放至目标分辨率的垂直大小
        scale = 1 - diff_y/s_size[1]  # 计算水平方向的缩放比例
        return int(s_size[0]*scale), t_size[1]


if __name__ == '__main__':
    for item in os.listdir('.'):
        if os.path.isfile(item) and imghdr.what(item):
            resize_image(item)
    pass
