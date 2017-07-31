#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/7/31 下午4:44
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : cmdline.py
# @Software: PyCharm
from scrapy import cmdline

__author__ = 'blackmatrix'

cmdline.execute("scrapy crawl apple".split())

if __name__ == '__main__':
    pass
