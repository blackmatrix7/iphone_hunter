#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/9/14 下午5:18
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : extensions.py
# @Software: PyCharm
from config import current_config
from tookit import RabbitMQ, Cache

__author__ = 'blackmatrix'

rabbit = RabbitMQ(config=current_config)

cache = Cache(config=current_config)

if __name__ == '__main__':
    pass
