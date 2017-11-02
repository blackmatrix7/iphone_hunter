#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/7/31 下午4:44
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : cmdline.py
# @Software: PyCharm
import os
import logging
from extensions import cache
from toolkit.cmdline import cmdline
from toolkit.initlogs import log_init

__author__ = 'blackmatrix'

# 初始化日志配置文件
log_init(file=os.path.abspath('logging.cfg'))

if __name__ == '__main__':

    if cmdline.command == 'hunter':
        logging.info('[猎手] 已运行')
        from hunter import hunting
        hunting()
    elif cmdline.command == 'falcon':
        logging.info('[猎鹰] 已运行')
        cache.delete('buyers')
        import falcon
        falcon.search_iphone()
    elif cmdline.command == 'courier':
        logging.info('[信使] 已运行')
        from courier import send_msg
        send_msg()
    elif cmdline.command == 'shoot':
        logging.info('[射手] 已运行')
        from hunter import quick_buy
        message = {'model': 'iPhone X', 'color': '深空灰色', 'space': '256GB', 'quantity': 1,
                   'store': 'R388', 'email': 'xxxxxxx@hotmail.com',
                   'apple_id': 'xxxxxxx@hotmail.com', 'apple_id_pass': 'XXXXXXXXXXX',
                   'first_name': '振', 'last_name': '李', 'idcard': '3708301989xxxxxxxx'}
        quick_buy(message)
