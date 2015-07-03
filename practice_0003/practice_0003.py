#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'


import random
import string
import redis

salt = "I"  # 分隔标志码
r = redis.StrictRedis(host='192.168.56.1', port=6379, db=0)
invite_code_nums = 200


def invite_code(invite_id, length=10):
    prefix = hex(invite_id)[2:] + salt
    chars = string.ascii_uppercase + string.digits
    char_count = length - len(prefix)
    return prefix + ''.join([random.choice(chars) for i in range(char_count)])


def get_invite_id(str_code):
    id_hex = str_code.split(salt)[0].upper()
    return int(id_hex, 16)


def put_code_redis(codes):
    for i, v in codes:
        r.hset('invite_code', i, v)  # 利用redis的 hash类型 进行存储


if __name__ == '__main__':
    my_codes = []
    for code_id in range(invite_code_nums):
        my_codes.append((code_id, invite_code(code_id)))
    put_code_redis(my_codes)
    for i in range(10):
        code_id = random.choice(range(invite_code_nums))
        # hscan操作可以进行游标定位，缓存key数量巨大的情况，利用cursor和count参数对该缓存进行组合多次迭代
        invite_code = r.hscan('invite_code', match=code_id, count=invite_code_nums)
        print('Invite:id--{}, code--{}'.format(code_id, invite_code))
