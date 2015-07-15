#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import string
import random

chars = string.ascii_letters + string.digits


def generate_image(size=(360, 90), quantity=4):
    """
    动态生成验证码图片, 存在BUG：如果字符颜色为白色或浅色比较坑爹，同时又字符被遮挡的情况
    :param size: tuple类型的图片大小
    :return: tuple对象，包含验证码字符和验证码图片
    """
    def get_random_font():  # 提供随机字体
        font_size = min(size)
        font_size = random.randint(font_size//2, font_size)
        return ImageFont.truetype(font="arial.ttf", size=font_size)

    def get_random_color(alpha=255):  # 提供随机颜色，透明度为参数
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = (r, g, b, alpha)
        return color

    def get_text_image():  # 返回验证码字符和验证码字符图片
        char = random.choice(chars)  # 随机字符
        font = get_random_font()  # 获取字体
        color = get_random_color()  # 获取随机颜色
        length = font.size * 2  # 获取字符背景画板的长和宽， 字体的两倍确保字体绘制时，不会被自动截掉
        text_im = Image.new('RGBA', (length, length), (255, 255, 255, 0))  # 创建透明的字符背景图
        draw = ImageDraw.Draw(text_im)  # 绘制字符
        draw.text((1, 1), char, fill=color, font=font)
        text_im = crop_text_image(text_im)
        text_im = convert_text_image(text_im)
        return char, text_im

    def crop_text_image(txt_img):  # 截掉字符图片多余的部分
        if len(txt_img.getbands()) != 4:
            return txt_img
        pixels_x = []
        pixels_y = []
        width, height = txt_img.size
        for x, y in ((x, y) for x in range(width) for y in range(height)):
            if txt_img.getpixel((x, y))[3] > 0:  # 透明度不为0，则为字符部分，否则为背景图部分
                pixels_x.append(x)
                pixels_y.append(y)
        crop_box = (min(pixels_x)-1, min(pixels_y)-1, max(pixels_x)+1, max(pixels_y)+1)
        return txt_img.crop(crop_box)

    def convert_text_image(txt_img):  # 为字符图片随机加纵向拉伸和旋转效果
        switch = random.randint(0, 4)
        x, y = txt_img.size
        stretch_y = random.randint(y, size[1])  # 随机拉伸长度
        angle = random.choice([random.randint(0, 30), random.randint(330, 360)])  # 随机选择角度
        if switch == 0:
            txt_img = txt_img.resize((x, stretch_y), resample=Image.LANCZOS)
        elif switch == 1:
            txt_img = txt_img.rotate(angle, resample=Image.BICUBIC, expand=1)
        elif switch == 2:
            txt_img = txt_img.resize((x, stretch_y), resample=Image.LANCZOS)
            txt_img = txt_img.rotate(angle, resample=Image.BICUBIC, expand=1)
            if txt_img.size[1] > size[1]:
                txt_img = txt_img.resize((txt_img.size[0], size[1]), resample=Image.LANCZOS)
        elif switch == 3:
            txt_img = txt_img.rotate(angle, resample=Image.BICUBIC, expand=1)
            txt_img = txt_img.resize((x, stretch_y), resample=Image.LANCZOS)
        temp_img = Image.new('RGBA', txt_img.size, (255, 255, 255, 255))
        return Image.alpha_composite(temp_img, txt_img)  # alpha_composite 方法避免paste时背景变黑的情况

    verification_img = Image.new('RGBA', size, (255, 255, 255, 255))
    verification_code = ''
    interval_x = size[0] // (quantity+1)
    for i in range(quantity):
        verification = get_text_image()
        verification_code += verification[0]
        paste_x = (i+1) * interval_x + random.choice([0, interval_x - verification[1].size[0]])
        paste_y = random.choice([0, size[1] - verification[1].size[1]])
        verification_img.paste(verification[1], (paste_x, paste_y))

    verification_img_draw = ImageDraw.Draw(verification_img)
    for _ in range(size[1]*100):  # 为验证码图片画噪点，数量是图片纵向长度的100倍
        point_x, point_y = random.randint(0, size[0]), random.randint(0, size[1])
        verification_img_draw.point((point_x, point_y), fill=get_random_color(200))  # 透明度设置为200
    verification_img.filter(ImageFilter.CONTOUR)  # 为验证码家过滤效果，感觉没什么效果
    verification_img.save('practice_0010.jpg', 'JPEG')
    return verification_code, verification_img


if __name__ == '__main__':
    print(generate_image())
    pass
