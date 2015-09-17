#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import os

__author__ = 'CityManager'

"""
计算程序文件中注释、空行、代码的行数
"""


def print_workload(path, ext='.py'):
    result = {
        'codes': 0,
        'commends': 0,
        'blanklines': 0
    }
    for root, dirs, files in os.walk(path):
        for f in files:
            if os.path.splitext(f)[1] == ext:
                commends, blanklines, codes = count_code_line(os.path.join(root, f))
                result['commends'] += commends
                result['blanklines'] += blanklines
                result['codes'] += codes
    print(result)


def count_code_line(filename):
    commends = 0
    blanklines = 0
    codes = 0
    is_comment = False
    with open(filename, 'rb') as f:
        for line in f:
            line = line.strip()
            if is_comment:
                commends += 1
                if line.endswith(b"'''") or line.endswith(b'"""'):
                    is_comment = False
            elif not line:
                blanklines += 1
            elif line.startswith(b'#'):
                commends += 1
            elif line.startswith(b"'''") or line.endswith(b'"""'):
                commends += 1
                is_comment = True
            else:
                codes += 1
    return commends, blanklines, codes


if __name__ == '__main__':
    # print(count_code_line('practice_0007.py'))
    print_workload(r'E:\pyspace\pyCharm\show-me-the-code')
