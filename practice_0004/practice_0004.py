#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

import string

letters = string.ascii_letters


def count_words(filename):
    result = dict()
    with open(filename, 'r') as f:
        items_list = (line.split() for line in f if line.split())
        for items in items_list:
            for str_item in items:
                word = check_word(str_item)
                if word in result:
                    result[word] += 1
                elif word:
                    result[word] = 1
    return result


def check_word(str_item):
    my_word = ''
    str_length = len(str_item)
    for i, v in enumerate(str_item):
        if v in letters or (v == "'" and i != 0 and i < str_length - 1):
            my_word += v
    if my_word:
        return my_word[0].upper() + my_word[1:].lower()


if __name__ == '__main__':
    for i, v in count_words('elementary.txt').items():
        print(i, " : ", v)
    pass
