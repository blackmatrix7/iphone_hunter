#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/7/31 下午4:44
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : cmdline.py
# @Software: PyCharm
import os
from config import current_config
from toolkit.cmdline import cmdline
from toolkit.initlogs import log_init

__author__ = 'blackmatrix'

# 初始化日志配置文件
log_init(file=os.path.abspath('logging.cfg'))

if __name__ == '__main__':

    if cmdline.command == 'hunter':
        from hunter import hunting
        if current_config['MULTIPROCESSING'] > 1:
            import multiprocessing
            pool = multiprocessing.Pool(processes=current_config['MULTIPROCESSING'])
            for i in range(current_config['MULTIPROCESSING']):
                pool.apply_async(hunting)
            pool.close()
            pool.join()
        else:
            hunting()
    elif cmdline.command == 'falcon':
        import falcon
        falcon.search_iphone()
    elif cmdline.command == 'courier':
        from courier import send_msg
        send_msg()
