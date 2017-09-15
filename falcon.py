#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 20:43
# @Author  : BlackMatrix
# @Site : 
# @File : falcon.py
# @Software: PyCharm
import requests
from time import sleep
from tookit import retry
from datetime import datetime
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
    while True:
        now = datetime.now()
        # 在有效的时间段内才查询库存
        if current_config.WATCH_START.hour <= now.hour <= current_config.WATCH_END.hour \
                and current_config.WATCH_START.minute <= now.minute <= current_config.WATCH_END.minute \
                and current_config.WATCH_START.second <= now.second <= current_config.WATCH_END.second:
            resp = requests.get(current_config['IPHONE_MODELS'])
            if resp.status_code == 200:
                return resp.json()
        sleep(5)

if __name__ == '__main__':
    pass
