#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

__author__ = 'CityManager'

from html.parser import HTMLParser
import urllib.request


class ZhihuHTMLParser(HTMLParser):
    is_target = False
    target_title = ['问题', '问题详情', '回答者', '回答内容']
    target_id = 0
    sub_tag = 0
    data = ''

    @staticmethod
    def get_value(atts, name):
        for key, value in atts:
            if key == name:
                return value
            else:
                return ""

    def handle_starttag(self, tag, attrs):
        tag_id = ZhihuHTMLParser.get_value(attrs, 'id')
        tag_class = ZhihuHTMLParser.get_value(attrs, 'class')
        if self.is_target:
            if tag == 'br':
                self.data += '\n'
            elif tag == 'img':
                self.data += ' '
            else:
                self.sub_tag += 1
        elif tag == 'div' and tag_id == 'zh-question-title':
            print("=================================================")
            self.is_target = True
            self.target_id = 0
        elif tag == 'div' and tag_id == 'zh-question-detail':
            self.is_target = True
            self.target_id = 1
        elif tag == 'h3' and tag_class == 'zm-item-answer-author-wrap':
            print("=================================================")
            self.is_target = True
            self.target_id = 2
        elif tag == 'div' and tag_class == 'fixed-summary zm-editable-content clearfix':
            self.is_target = True
            self.target_id = 3

    def handle_data(self, data):
        if self.is_target:
            self.data += data.strip()

    def handle_endtag(self, tag):
        if tag in ('br', 'img'):
            return
        if self.is_target and self.sub_tag == 0:
            self.is_target = False
            print('{}:\n{}'.format(self.target_title[self.target_id], self.data))
            if self.target_id in (1, 3):
                print("=================================================")
            self.data = ''
            self.target_id = 0
        elif self.is_target and self.sub_tag > 0:
            self.sub_tag -= 1
            # print('end', tag, self.sub_tag)


if __name__ == '__main__':
    f = urllib.request.urlopen(r'http://www.zhihu.com/question/22866524')
    parser = ZhihuHTMLParser()
    response = f.read().decode('utf-8')
    parser.feed(response)
    f.close()
