#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 20:43
# @Author  : BlackMatrix
# @Site : 
# @File : falcon.py
# @Software: PyCharm
import json
import requests
from time import sleep
from toolkit import retry
from datetime import datetime
from config import current_config
from extensions import cache, rabbit

__author__ = 'blackmatrix'


@cache.cached('buyers')
def get_buyers_info():
    """
    获取并整理买家信息，按零售店划分
    :return:
    """
    buyers = {}
    for buyer in current_config['BUYERS']:
        buy_stores = []

        # 获取意向购买城市的零售店
        if buyer.get('city') is not None:
            buy_stores.extend(get_apple_stores(buyer['city']).keys())
        # 追加特别指定的零售店
        if buyer.get('stores') is not None:
            buy_stores.extend(buyer['stores'])
        # 零售店去重
        buy_stores = set(buy_stores)

        for buy_store in buy_stores:
            store = buyers.setdefault(buy_store, {})
            # 获取意向购买的型号
            for buy_model in buyer['models']:
                model_number = current_config['MODELS'].get('{0} {1} {2}'.format(*buy_model))
                buy_info = {k: v for k, v in buyer.items() if k in ('last_name', 'first_name', 'idcard', 'quantity',)}
                buy_info.update({'model': buy_model[0], 'color': buy_model[1], 'space': buy_model[2]})
                store.setdefault(model_number, []).append(buy_info)
    return buyers


@cache.cached('apple_stores')
@retry(max_retries=10)
def get_apple_stores(select_city=None):
    """
    获取所有的Apple Store信息，并按城市分类
    也可以获取单个城市的零售店信息
    :return:
    """
    stores = {}
    resp = requests.get(current_config['APPLE_STORES_URL'])
    for store in resp.json()['stores']:
        if store['enabled'] is True:
            city = stores.setdefault(store['city'], {})
            city.update({store['storeNumber']: store['storeName']})
    if select_city is None:
        return stores
    else:
        return stores[select_city]


@retry(max_retries=3)
def search_iphone():
    rabbit.connect()
    while True:
        sleep(5)
        # 购买者的信息，每次循环实时获取最新的购买者信息
        buyers_info = get_buyers_info()
        now = datetime.now().time()
        # 在有效的时间段内才查询库存
        if current_config['WATCH_START'] <= now <= current_config['WATCH_END']:
            resp = requests.get(current_config['IPHONE_MODELS_URL'])
            availability = resp.json()
            # 遍历意向购买的商店和意向购买的商品
            for store, models in buyers_info.items():
                # 遍历意向购买的型号和对应的购买人
                for model_number, buyers in models.items():
                    # 获取商品型号在店内的库存
                    stock = availability['stores'][store][model_number]
                    if stock['availability']['unlocked'] is True:
                        buy_info = buyers_info[store][model_number][0]
                        hash_key = hash(json.dumps(buy_info))
                        if cache.get(hash_key) is None:
                            # 已经发送过的购买者信息，5分钟内不再发送
                            cache.set(key=hash_key, val=True, time=300)
                            buy_info['store'] = store
                            rabbit.send_message(exchange_name='iphone', queue_name='buyer', messages=buy_info)

if __name__ == '__main__':
    pass
