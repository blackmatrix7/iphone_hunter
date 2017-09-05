#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 20:43
# @Author  : BlackMatrix
# @Site : 
# @File : falcon.py
# @Software: PyCharm
import requests
from config import current_config
__author__ = 'blackmatrix'


def search_iphone():
    resp = requests.get(current_config['IPHONE_MODELS'])
    if resp.status_code == 200:
        return resp.json()

if __name__ == '__main__':
    pass
