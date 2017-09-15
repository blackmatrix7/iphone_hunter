#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/7/31 下午10:19
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: config
# @Software: PyCharm
import os
from datetime import datetime
from tookit import BaseConfig, get_current_config

__author__ = 'blackmatrix'


class CommonConfig(BaseConfig):

    # 项目路径
    PROJ_PATH = os.path.abspath('')

    # Apple Store Url
    APPLE_STORES_URL = 'https://reserve-cn.apple.com/CN/zh_CN/reserve/iPhone/stores.json'
    IPHONE_MODELS_URL = 'https://reserve-cn.apple.com/CN/zh_CN/reserve/iPhone/availability.json'

    # 购买者信息
    BUYERS = [
        {
            'first_name': '三', 'last_name': '张', 'idcard': 'xxxxxxxxx',
            'city': 'shanghai', 'stores': ['R607', 'R345'],
            'models':
                (
                    ['iPhone 8', '深空灰色', '64G'],
                    ['iPhone 8', '金色', '64G']
                )
        },
        {
            'first_name': '四', 'last_name': '李', 'idcard': 'xxxxxxxxx',
            'city': 'beijing', 'stores': ['R633', 'R797'],
            'models':
                (
                    ['iPhone 8 Plus', '银色', '256G'],
                    ['iPhone 8', '深空灰色', '64G']
                )
        }
    ]

    # 购买时间段
    WATCH_START = datetime.strptime('7:40:00', '%H:%M:%S').time()
    WATCH_END = datetime.strptime('20:40:00', '%H:%M:%S').time()

    APPLE_INDEX = 'https://www.apple.com/cn/'
    APPLE_FLYOUT_AJAX = 'https://www.apple.com/cn/shop/bag/flyout?apikey={}&l=https%3A%2F%2Fwww.apple.com%2Fcn%2F'
    APPLE_SING_IN = 'https://{}/cn/shop/sentryx/sign_in'

    API_KEY_XPATH = '//*[@name="ac-gn-store-key"]/@content'
    APPLE_ID_XPATH = '//*[@id="sign-in-content"]'
    APPLE_ID_PASS_XPATH = '//*[@id="login-password"]'

    # selenium 配置
    # 全局超时时间
    TIME_OUT = 60
    # 轮询间隔
    POLL_FREQUENCY = 0.2
    # 进程数，不建议超过CPU核数
    MULTIPROCESSING = 4

    # GAMMU
    FILECONFIG = os.path.abspath('.gammurc')

    # RabbitMQ
    RABBITMQ_HOST = '127.0.0.1'
    RABBITMQ_PORT = 5672
    RABBITMQ_USER = 'user'
    RABBITMQ_PASS = '123456'

    @property
    def apple_stores(self):
        stores = {'shanghai': ['R607', 'R345'],
                  'beijing': ['R633', 'R797']}
        return stores

    @staticmethod
    def get_buy_url(model, color, space):
        model_code = {
            'iPhone 8': '00',
            'iPhone 8 Plus': '01',
        }.get(model, '01')

        model_name = {
            'iPhone 8': '4.7-英寸屏幕',
            'iPhone 8 Plus': '5.5-英寸屏幕',
        }.get(model, '5.5-英寸屏幕')

        color_code = {
            '银色': '10',
            '金色': '11',
            '深空灰色': '12'
        }.get(color, '11')
        space_code = {
            '64GB': '20',
            '256GB': '21'
        }.get(space, '20')

        buy_url = 'https://www.apple.com/cn/shop/buy-iphone/iphone-8/' \
                  '{model_name}-{space}-{color}#' \
                  '{model_code},{color_code},{space_code}'.format(model_name=model_name,
                                                                  space=space,
                                                                  color=color,
                                                                  model_code=model_code,
                                                                  color_code=color_code,
                                                                  space_code=space_code)
        return buy_url

    # 统一命名
    APPLE_STORES = apple_stores

commoncfg = CommonConfig()

configs = {
    'default': commoncfg
}

# 读取配置文件的名称，在具体的应用中，可以从环境变量、命令行参数等位置获取配置文件名称
config_name = 'default'

current_config = get_current_config(config_name)
