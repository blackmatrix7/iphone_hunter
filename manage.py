#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/7/31 下午4:44
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : cmdline.py
# @Software: PyCharm
import falcon
from hunter import Shoot
from extensions import rabbit
from config import current_config
from tookit.cmdline import cmdline

__author__ = 'blackmatrix'


def hunting():

    # 为每个进程单独打开一个浏览器
    shoot = Shoot()

    # 从消息队列获取订购信息，如果
    @rabbit.receive_from_rabbitmq(exchange_name='iphone', queue_name='buyer', routing_key='apple')
    def start():
        shoot.select_iphone('R607')
        # apple_stores = falcon.get_apple_stores()
        # iphone_stock = falcon.search_iphone()
        # for watch_store_key, watch_store_value in iphone_stock.items():
        #     # TODO 判断库存是否有需要购买的型号
        #     pass
        # quick_buy.select_iphone('R607')
    start()


if __name__ == '__main__':

    if cmdline.command == 'hunter':
        import multiprocessing
        pool = multiprocessing.Pool(processes=current_config.MULTIPROCESSING)
        for i in range(current_config.MULTIPROCESSING):
            pool.apply_async(hunting)
        pool.close()
        pool.join()
    elif cmdline.command == 'falcon':
        falcon.search_iphone()
    elif cmdline.command == 'courier':
        pass
