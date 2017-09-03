#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/7/31 下午4:44
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : cmdline.py
# @Software: PyCharm
from scrapy import cmdline
from hunter.spiders import shotgun

__author__ = 'blackmatrix'


# spider = shotgun.AppleSpider()
#
# resp = spider.shoot()
#
# print(resp)

cmdline.execute("scrapy crawl apple".split())

if __name__ == '__main__':
    pass
