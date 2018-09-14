#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 20:43
# @Author  : BlackMatrix
# @Site : 
# @File : falcon.py
# @Software: PyCharm
import pickle
import logging
from time import sleep
from toolkit import retry
from datetime import datetime
from config import current_config
from extensions import cache, rabbit, r

__author__ = 'blackmatrix'


def get_model_number(model_name):
    try:
        model_number = current_config['MODELS'][model_name]
        return model_number
    except KeyError:
        raise KeyError('没有找到匹配的型号，请检查参数配置。')


@cache.cached('buyers', 172800)
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
                model_number = get_model_number('{0} {1} {2}'.format(buy_model['model'],
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
    except (Exception, FileNotFoundError):
        stores = {}
        resp = r.get(current_config['APPLE_STORES_URL'])
        for store in resp.json()['stores']:
            if store['enabled'] is True:
                city = stores.setdefault(store['city'], {})
                city.update({store['storeNumber']: store['storeName']})
        file = open('stores', 'wb')
        pickle.dump(stores, file)
    return stores if select_city is None else stores.get(select_city)


def get_store_name(store_code):
    """
    根据Apple Store编号获取名称
    :param store_code: 
    :return: 
    """
    stores = get_apple_stores()
    for city, store in stores.items():
        for code, name in store.items():
            if code == store_code:
                return name


def get_model_name(part_num):
    """
    根据型号获取设备名称
    :param part_num: 
    :return: 
    """
    models = current_config.MODELS
    for model_name, model_part_num in models.items():
        if model_part_num == part_num:
            return model_name


def search_iphone():
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
                    for buyer in buyers:
                        key = '{}{}{}'.format(buyer['idcard'], store, model_number)
                        if cache.get(key) is None:
                            buyer['store'] = store
                            # with rabbit as mq:
                            #     mq.send_message(exchange_name='iphone', queue_name='buyers', messages=buyer)
                            # 日志记录及微信消息发送
                            msg = '发现有效库存，商店【{0}】， 型号【{1}】，时间【{2}】。'.format(get_store_name(store),
                                                                            get_model_name(model_number),
                                                                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                            r.get(' http://sc.ftqq.com/{}.send?text=您关注的iPhone已有库存&desp={}'.format(
                                current_config.SEC_KEY, msg))
                            logging.info(msg)
                            logging.info('买家信息：{}'.format(buyer))
                            logging.info('[猎鹰] 已将目标设备和买家信息发送给猎手')
                            # 已经发送过的购买者信息，5分钟内不再发送
                            cache.set(key=key, val='已发送', time=180)
        else:
            logging.info('[猎鹰] 没有发现有效库存')


@retry(max_retries=60, step=0.5, callback=logging.error)
def start():
    logging.info('[猎鹰] 开始监控设备库存信息')
    # 清理缓存
    cache.flush_all()
    while True:
        now = datetime.now().time()
        # 在有效的时间段内才查询库存
        if current_config['WATCH_START'] <= now <= current_config['WATCH_END']:
            search_iphone()
            sleep(2)


if __name__ == '__main__':
    pass
