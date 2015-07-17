#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

from openpyxl import Workbook
import json


class Student(object):
    def __init__(self, sid, info):
        self.sid = int(sid)
        self.name = info[0]
        self.math_score = info[1]
        self.chinese_score = info[2]
        self.english_score = info[3]

    def into_row(self):
        return [self.sid, self.name, self.math_score, self.chinese_score, self.english_score]

    def __str__(self):
        return '%s' % self.into_row()

    def __repr__(self):
        return self.__str__()


def json2students(j_dict):
    students = []
    for k, v in j_dict.items():
        students.append(Student(k, v))
    students.sort(key=lambda student: student.sid)
    return students


def get_students(filename):
    with open(filename, 'rb') as f:
        students = f.read().decode()
    students = json.loads(students, object_hook=json2students)
    return students


def save_students(stu_list, filename):
    wb = Workbook()
    wb.create_sheet(0, "student")
    ws = wb.active
    for stu in stu_list:
        ws.append(stu.into_row())
    wb.save(filename)


if __name__ == '__main__':
   save_students(get_students('student.txt'), 'student_more.xlsx')
