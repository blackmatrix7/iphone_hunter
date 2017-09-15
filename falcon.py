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
@retry(max_retries=10)
def get_apple_stores():
    """
    获取所有的Apple Store信息，并按城市分类
    :return:
    """
    stores = {}
    resp = requests.get(current_config['APPLE_STORES_URL'])
    for store in resp.json()['stores']:
        if store['enabled'] is True:
            city = stores.setdefault(store['city'], [])
            city.append({store['storeNumber']: store['storeName']})
    return stores


@retry(max_retries=3)
def search_iphone():
    while True:
        now = datetime.now().time()
        # 在有效的时间段内才查询库存
        if current_config['WATCH_START'] <= now <= current_config['WATCH_END']:
            resp = requests.get(current_config['IPHONE_MODELS_URL'])
            availability = resp.json()
            for store in availability['stores']:
                pass
        sleep(5)

if __name__ == '__main__':
    pass
