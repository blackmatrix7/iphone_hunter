#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/7/31 下午4:44
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : cmdline.py
# @Software: PyCharm
import falcon
from shoot import QuickBuy
__author__ = 'blackmatrix'

# quick_buy = QuickBuy()


def hunting():
    while True:
        apple_stores = falcon.get_apple_stores()
        iphone_stock = falcon.search_iphone()
        for watch_store_key, watch_store_value in iphone_stock.items():
            # TODO 判断库存是否有需要购买的型号
            pass
        # quick_buy.select_iphone('R607')

if __name__ == '__main__':

    hunting()
