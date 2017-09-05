#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/7/31 下午10:19
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: config
# @Software: PyCharm
from tookit import BaseConfig

__author__ = 'blackmatrix'


class CommonConfig(BaseConfig):

    # Apple Store Url
    APPLE_STORES = 'https://reserve-cn.apple.com/CN/zh_CN/reserve/iPhone/stores.json'
    IPHONE_MODELS = 'https://reserve-cn.apple.com/CN/zh_CN/reserve/iPhone/availability.json'
    BUY_PAGE = 'https://reserve-cn.apple.com/CN/zh_CN/reserve/iPhone/availability?channel=1'

basecfg = CommonConfig()

configs = {
    'basecfg': basecfg
}

config_name = 'default'
try:
    import localconfig
    current_config = localconfig.configs[config_name]
except ImportError:
    current_config = configs[config_name]