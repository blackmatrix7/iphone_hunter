#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 20:43
# @Author  : BlackMatrix
# @Site : 
# @File : falcon.py
# @Software: PyCharm
import os
import pickle
import logging
from time import sleep
from toolkit import retry
from datetime import datetime
from config import current_config
from extensions import cache, rabbit, r

__author__ = 'blackmatrix'


@cache.cached('buyers', timeout=345600)
@retry(max_retries=60, sleep=1, callback=logging.error)
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
            logging.info('[猎鹰] 买家目标城市：{}'.format(buyer.get('city')))
            city_stores = list(get_apple_stores(buyer['city']).keys())
            logging.info('[猎鹰] {0}全部Apple Store：{1}'.format(buyer.get('city'), city_stores))
            buy_stores.extend(city_stores)
        # 追加特别指定的零售店
        if buyer.get('stores') is not None:
            buy_stores.extend(buyer['stores'])
        # 零售店去重
        buy_stores = set(buy_stores)

        for buy_store in buy_stores:
            store = buyers.setdefault(buy_store, {})
            # 获取意向购买的型号
            for buy_model in buyer['models']:
                model_number = current_config['MODELS'].get('{0} {1} {2}'.format(buy_model['model'],
                                                                                 buy_model['color'],
                                                                                 buy_model['space']))
                buy_info = {k: v for k, v in buyer.items() if k in ('last_name', 'first_name', 'idcard',
                                                                    'apple_id', 'apple_id_pass', 'email')}
                buy_info.update({
                    'model': buy_model['model'],
                    'color': buy_model['color'],
                    'space': buy_model['space'],
                    'quantity': buy_model['quantity']
                })
                store.setdefault(model_number, []).append(buy_info)
    return buyers


@retry(max_retries=60, sleep=1, callback=logging.error)
def get_apple_stores(select_city=None):
    """
    获取所有的Apple Store信息，并按城市分类
    也可以获取单个城市的零售店信息
    :return:
    """
    try:
        file = open('stores', 'rb')
        stores = pickle.load(file)
    except EOFError:
        stores = {}
        resp = r.get(current_config['APPLE_STORES_URL'])
        for store in resp.json()['stores']:
            if store['enabled'] is True:
                city = stores.setdefault(store['city'], {})
                city.update({store['storeNumber']: store['storeName']})
        file = open('stores', 'wb')
        pickle.dump(stores, file)
    logging.info('[猎鹰] 正在获取{}的Apple Store'.format(select_city))
    return stores if select_city is None else stores.get(select_city)


@retry(max_retries=60, step=0.5, callback=logging.error)
def search_iphone():
    logging.info('[猎鹰] 开始监控设备库存信息')
    while True:
        now = datetime.now().time()
        # 在有效的时间段内才查询库存
        if current_config['WATCH_START'] <= now <= current_config['WATCH_END']:
            # 购买者的信息，每次循环实时获取最新的购买者信息
            buyers_info = get_buyers_info()
            availability = r.get(current_config['IPHONE_MODELS_URL']).json()
            if availability['stores']:
                # 遍历意向购买的商店和意向购买的商品
                for store, models in buyers_info.items():
                    # 遍历意向购买的型号和对应的购买人
                    for model_number, buyers in models.items():
                        # 获取商品型号在店内的库存
                        stock = availability['stores'][store][model_number]
                        if stock['availability']['unlocked'] is True:
                            logging.info('[猎鹰] 发现目标设备有效库存，商店:{0}， 型号{1}'.format(store, model_number))
                            for buyer_info in buyers_info[store][model_number]:
                                if cache.get(buyer_info['idcard']) is None:
                                    buyer_info['store'] = store
                                    with rabbit as mq:
                                        mq.send_message(exchange_name='iphone', queue_name='buyers', messages=buyer_info)
                                    logging.info('买家信息：{}'.format(buyer_info))
                                    logging.info('[猎鹰] 已将目标设备和买家信息发送给猎手')
                                    # 已经发送过的购买者信息，5分钟内不再发送
                                    cache.set(key=buyer_info['idcard'], val=True, time=300)
                else:
                    logging.info('[猎鹰] 没有发现有效库存')
            sleep(3)


if __name__ == '__main__':
    pass
