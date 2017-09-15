#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/7/31 下午4:44
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : cmdline.py
# @Software: PyCharm
import falcon
from hunter import hunting
from config import current_config
from tookit.cmdline import cmdline

__author__ = 'blackmatrix'


if __name__ == '__main__':

    if cmdline.command == 'hunter':
        import multiprocessing
        pool = multiprocessing.Pool(processes=current_config['MULTIPROCESSING'])
        for i in range(current_config['MULTIPROCESSING']):
            pool.apply_async(hunting)
        pool.close()
        pool.join()
    elif cmdline.command == 'falcon':
        falcon.search_iphone()
    elif cmdline.command == 'courier':
        pass
