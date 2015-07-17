#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

from openpyxl import Workbook


def get_numbers(filename):
    txt = ''
    with open(filename, 'rb') as f:
        for line in f:
            txt += line.decode().strip()
    return eval(txt)


def save_numbers(numbers_list, filename):
    wb = Workbook()
    wb.create_sheet(0, 'numbers')
    ws = wb.active
    for numbers in numbers_list:
        ws.append(numbers)
    wb.save(filename)


if __name__ == '__main__':
    save_numbers(get_numbers('numbers.txt'), 'numbers.xlsx')
