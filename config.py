#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/7/31 下午10:19
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: config
# @Software: PyCharm
import os
from tookit import BaseConfig

__author__ = 'blackmatrix'


class CommonConfig(BaseConfig):

    # Apple Store Url
    APPLE_STORES = 'https://reserve-cn.apple.com/CN/zh_CN/reserve/iPhone/stores.json'
    IPHONE_MODELS = 'https://reserve-cn.apple.com/CN/zh_CN/reserve/iPhone/availability.json'
    BUY_PAGE = 'https://reserve-cn.apple.com/CN/zh_CN/reserve/iPhone/availability?channel=1'

    APPLE_INDEX = 'https://www.apple.com/cn/'
    APPLE_FLYOUT_AJAX = 'https://www.apple.com/cn/shop/bag/flyout?apikey={}&l=https%3A%2F%2Fwww.apple.com%2Fcn%2F'
    APPLE_SING_IN = 'https://{}/cn/shop/sentryx/sign_in'

    API_KEY_XPATH = '//*[@name="ac-gn-store-key"]/@content'
    APPLE_ID_XPATH = '//*[@id="sign-in-content"]'
    APPLE_ID_PASS_XPATH = '//*[@id="login-password"]'

    # 项目路径
    PROJ_PATH = os.path.abspath('')
    # 全局超时时间
    TIME_OUT = 20

commoncfg = CommonConfig()

configs = {
    'default': commoncfg
}

# 读取配置文件的名称，在具体的应用中，可以从环境变量、命令行参数等位置获取配置文件名称
config_name = 'default'

current_config = get_current_config(config_name)
