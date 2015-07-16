#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

filtered_words = []
with open('filtered_words.txt', 'rb') as f:
    for line in f:
        filtered_words.append(line.decode('utf-8').strip())

while True:
    input_line = input("请输入关键词汇:\n").strip()

    for filtered_word in filtered_words:
        input_line = input_line.replace(filtered_word, len(filtered_word) * '*')

    print(input_line)
    if input_line == 'exit':
        break
