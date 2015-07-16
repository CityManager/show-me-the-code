#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

import urllib.request
from html.parser import HTMLParser


def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'}
    req = urllib.request.Request(url=url, headers=headers)  # 模拟通过火狐浏览器发送请求
    page = urllib.request.urlopen(req)
    html = page.read()
    with open('html_jd.txt', 'wb') as f:
        f.write(html)
    return html.decode('utf-8')


class ImgParser(HTMLParser):
    img_url_list = []

    @staticmethod
    def get_att_value(atts, name):
        for key, value in atts:
            if key == name:
                return value
        else:
                return None

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            src = ImgParser.get_att_value(attrs, 'src')
            org_src = ImgParser.get_att_value(attrs, 'org_src')
            if org_src:
                self.img_url_list.append(org_src)
            elif src:
                self.img_url_list.append(src)

    def get_img_url_list(self):
        return self.img_url_list


def get_img(img_url_list):
    i = 0
    for img_url in img_url_list:
        urllib.request.urlretrieve(img_url, "%s.jpg" % i)
        i += 1


if __name__ == '__main__':
    imgP = ImgParser()
    imgP.feed(get_html(r'http://jandan.net/pic/page-6935'))
    get_img(imgP.get_img_url_list())

