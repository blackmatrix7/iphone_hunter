#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 20:43
# @Author  : BlackMatrix
# @Site : 
# @File : falcon.py
# @Software: PyCharm
import requests
from tookit import retry
from functools import lru_cache
from config import current_config

__author__ = 'blackmatrix'


@lru_cache(maxsize=5)
@retry(max_retries=3)
def get_apple_stores():
    resp = requests.get(current_config['APPLE_STORES'])
    if resp.status_code == 200:
        return resp.json()


@retry(max_retries=3)
def search_iphone():
    resp = requests.get(current_config['IPHONE_MODELS'])
    if resp.status_code == 200:
        return resp.json()

if __name__ == '__main__':
    pass
