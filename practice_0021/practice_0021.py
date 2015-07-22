#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

import pymysql
import hashlib
import os
import re
import base64

"""
对密码进行hash，而后再进行base64解码
"""

RANDOM_NUM = 10
ALT_CHARS = b'Aa'


def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(RANDOM_NUM)
    result = salt + hashlib.sha256(password.encode('utf-8')+salt).digest()
    return base64.b64encode(result, altchars=ALT_CHARS).decode('utf-8')  # 返回字符串类型的密码


def check_password(hashed_password, user_password):
    print(type(hashed_password))
    salt = base64.b64decode(hashed_password, altchars=ALT_CHARS)[:RANDOM_NUM]
    print(type(salt))
    return hashed_password == hash_password(user_password, salt=salt)


def get_user(username):
    conn = pymysql.connect(host="192.168.56.1", port=3306, user='pyuser', passwd='gmcc1234', db='pysql')
    try:
        with conn.cursor() as cursor:
            sql = "select username, password from user where username='%s'" % username
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                username, password = result
                return username, password
            else:
                return None
    finally:
        conn.close()


def save_user(username, password):
    password = hash_password(password)
    conn = pymysql.connect(host="192.168.56.1", port=3306, user='pyuser', passwd='gmcc1234', db='pysql')
    try:
        with conn.cursor() as cursor:
            sql = "select username, password from user where username= '%s'" % username
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                sql = 'update user set password = "%s" where username = "%s"' % (username, password)
            else:
                sql = 'insert into user(username, password) values ("%s", "%s")' % (username, password)
            cursor.execute(sql)
            conn.commit()
    finally:
        conn.close()


def main():
    print("欢迎访问，请根据指令输入内容，谢谢")
    reg = r"[a-zA-Z][0-9a-zA-Z\_]*"
    username_re = re.compile(reg)
    while True:
        username = input("请输入用户名:")
        if not re.fullmatch(username_re, username) or len(username) > 40:
            print("请确保用户名字母开头并且只包含字母数字和下划线，用户名长度不能超过40个字符")
            continue
        else:
            break

    while True:
        password = input("请输入密码:")
        if not password or len(password) > 40:
            print("请确保密码位数不为0或者不超过40位")
            continue
        else:
            break
    user = get_user(username)
    if not user:
        save_user(username, password)
        print("嘿嘿，注册成功，欢迎您，%s" % username)
    else:
        print(type(user[1]))
        if check_password(user[1], password):
            print("登陆成功，欢迎您，%s" % username)
        else:
            print('密码错误，程序退出！')


if __name__ == '__main__':
    pd = hash_password('hello1')
    print('haha', pd)
    print(len(pd))
    print(type(pd))
    print(check_password(pd, 'hello1'))
    main()
