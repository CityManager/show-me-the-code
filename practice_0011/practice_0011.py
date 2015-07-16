#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

filtered_words = []
with open('filtered_words.txt', 'rb') as f:
    for line in f:
        filtered_words.append(line.decode('utf-8').strip())

while True:
    input_line = input("请输入关键词汇:\n")
    is_right = True

    for filtered_word in filtered_words:
        if filtered_word in input_line:
            is_right = False
            break

    if is_right:
        print('Human Rights')
    else:
        print('freedom')

    if input_line.strip() == 'exit':
        break
