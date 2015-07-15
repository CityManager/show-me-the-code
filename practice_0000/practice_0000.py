#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
from PIL import ImageFont


def mask_num_circle(image_s, num=0):
    """
    为头像图片添加未读信息提示
    :param image_s: 头像图片PIL.Image对象
    :param num: 未读信息条数
    :return: PIL.Image对象，添加未读信息标示的头像图片
    """
    # 底层背景
    size_x, size_y = image_s.size
    padding_x, padding_y = size_x//15, size_y//15  # 预留padding
    im_size_x, im_size_y = size_x+padding_x, size_y+padding_y  # 背景的大小
    image_t = Image.new("RGBA", (im_size_x, im_size_y), color=(0, 0, 0, 0))  # 0才是透明

    # 贴入原图
    image_t.paste(image_s, (0, padding_y, size_x, im_size_y))

    # 画圆
    diameter = min(size_x, size_y)//3  # 圆的直径
    radius = diameter//2  # 圆的不精确半径
    color_red = ImageColor.getrgb('red')
    draw = ImageDraw.Draw(image_t)
    draw.ellipse([(im_size_x - diameter, 0), (im_size_x, diameter)], fill=color_red, outline=color_red)
    # 在圆上画数字
    num = str(num)
    color_white = ImageColor.getrgb('white')
    font = ImageFont.truetype(font="arial.ttf", size=radius)  # 设置字体大小为半径值
    font_size = font.getsize(num)  # 获取写入内容的大小
    font_x, font_y = font_size[0]//2 + font_size[0]//100, font_size[1]//2 + font_size[1]//10  # 估计margin或padding宽度
    text_position = (im_size_x - radius - font_x, radius - font_y)  # 尽量让文本画在中心
    draw.text(text_position, num, font=font, fill=color_white)
    return image_t


if __name__ == "__main__":
    with Image.open("321.jpg") as im:
        mask_num_circle(im, 14).save("test.png", "PNG")  # 保存成png格式，才能实现透明背景
