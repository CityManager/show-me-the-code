#!/usr/bin/env python
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

import random
import string

salt = "I"  # 分隔标志码


def invite_code(invite_id, length=10):
    """
    ID + salt + 随机码方式
    随机码通过 random.choice(字母数字集) 获得
    :param invite_id: 邀请码表id
    :param length: 邀请码设置长度
    :return: 邀请码
    """
    prefix = hex(invite_id)[2:] + salt
    chars = string.ascii_letters + string.digits  # string模块字母和数字
    char_count = length - len(prefix)  # 剩余待补充字符长度
    return prefix + ''.join([random.choice(chars) for i in range(char_count)])  # 生成式,i可以不使用


def get_invite_id(str_code):
    """
    从邀请码中解析出邀请码表id
    :param str_code: 邀请码
    :return: 邀请码表id，int类型
    """
    id_hex = str_code.split(salt)[0].upper()  # 获得大写id hex值
    return int(id_hex, 16)


if __name__ == '__main__':
    for i in range(10, 500, 17):
        code = invite_code(i)
        code_id = get_invite_id(code)
        print(code, code_id)
