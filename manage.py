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
        from extensions import r
        # 模拟 GET 请求
        resp1 = r.get('https://reserve-prime.apple.com/CN/zh_CN/reserve/iPhoneX?quantity=1&store=R389&partNumber=MQA62CH%2FA&channel=1&sourceID=&iUID=&iuToken=&iUP=N&appleCare=&rv=&path=&plan=unlocked', allow_redirects=False)

        print(resp1.headers['Location'])
