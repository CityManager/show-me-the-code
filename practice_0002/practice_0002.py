#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

import mysql.connector
import random
import string

create_sql = '''
create table invitation_code(
    id int primary key,
    code varchar(32) not null,
    valid tinyint not null default 1
)
'''

salt = "I"  # 分隔标志码
invite_code_nums = 200


def storage_invite_code(codes):
    """
    将邀请码保存到mysql数据库中。
    :param codes: 邀请码list集合
    :return: None
    """
    conn = mysql.connector.connect(host='192.168.56.1', port=3306, user='pyuser', password='gmcc1234', database='pysql')
    try:
        cursor = conn.cursor()
        cursor.execute("select count(*) from information_schema.tables where table_name = 'invitation_code'")
        table_exits = cursor.fetchone()[0]
        if not table_exits:  # 如果表不存在，则建表
            cursor.execute(create_sql)
            conn.commit()
        for i, v in codes:  # 将数据插入库表
            cursor.execute("insert into invitation_code (id, code) values (%s, %s)", (i, v))
        conn.commit()
        cursor.close()
    finally:
        conn.close()


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
    my_codes = []
    for code_id in range(invite_code_nums):
        my_codes.append((code_id, invite_code(code_id)))
    storage_invite_code(my_codes)
