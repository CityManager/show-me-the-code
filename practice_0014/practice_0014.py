#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

from openpyxl import Workbook
import json


def get_student_info(filename):
    with open(filename, 'rb') as f:
        students = f.read().decode()
    stu_dict = json.loads(students)
    return stu_dict


def save_student_info(stu_dict, filename):
    wb = Workbook()
    wb.create_sheet(0, "student")
    ws = wb.active

    keys = list()
    for k in stu_dict:
        keys.append(k)
    keys.sort()  # 排序
    for k in keys:
        l = list()
        l.append(k)
        l.extend(stu_dict[k])
        ws.append(l)

    wb.save(filename)


if __name__ == '__main__':
    student_dict = get_student_info('student.txt')
    save_student_info(student_dict, 'student.xlsx')
