#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/9/14 下午5:18
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : extensions.py
# @Software: PyCharm
import requests
from config import current_config
from toolkit import RabbitMQ, Cache

__author__ = 'blackmatrix'

rabbit = RabbitMQ(config=current_config)

cache = Cache(config=current_config)

r = requests.Session()
r.headers.update(
    {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
     'accept-encoding': 'gzip, deflate, sdch, br',
     'accept-language': 'zh-CN,zh;q=0.8',
     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
     })

if __name__ == '__main__':
    pass
