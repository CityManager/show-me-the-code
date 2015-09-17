#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import urllib.request
import re

__author__ = 'CityManager'


def get_html(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    with open('html.txt', 'wb') as f:
        f.write(html)
    return html.decode('utf-8')


def get_img(html):
    reg = r'src="(.*?\.jpg)" bdwater='
    img_re = re.compile(reg)
    img_list = re.findall(img_re, html)
    i = 0
    for img_url in img_list:
        urllib.request.urlretrieve(img_url, "%s.jpg" % i)
        i += 1
        print(img_url)


if __name__ == "__main__":
    get_img(get_html(r'http://tieba.baidu.com/p/2166231880'))
