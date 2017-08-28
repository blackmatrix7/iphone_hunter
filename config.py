#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/7/31 下午10:19
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: config
# @Software: PyCharm
import os
__author__ = 'blackmatrix'


class BaseConfig:

    APPLE_INDEX = 'https://www.apple.com/cn/'
    APPLE_FLYOUT_AJAX = 'https://www.apple.com/cn/shop/bag/flyout?apikey={}&l=https%3A%2F%2Fwww.apple.com%2Fcn%2F'
    APPLE_SING_IN = 'https://{}/cn/shop/sentryx/sign_in'

    API_KEY_XPATH = '//*[@name="ac-gn-store-key"]/@content'
    APPLE_ID_XPATH = '//*[@id="sign-in-content"]'
    APPLE_ID_PASS_XPATH = '//*[@id="login-password"]'

    APPLE_ID = os.environ.get('APPLE_ID')
    APPLE_ID_PASS = os.environ.get('APPLE_ID_PASS')

    def __setitem__(self, key, value):
        raise AttributeError

    def __delitem__(self, key):
        raise AttributeError

    def __getitem__(self, item):
        return getattr(self, item)

    def get(self, item, value=None):
        return getattr(self, item, value)


basecfg = BaseConfig()

config = {
    'basecfg': basecfg
}

config_name = cmdline.config
try:
    import localconfig
    current_config = localconfig.configs[config_name]
except ImportError:
    current_config = configs[config_name]

if __name__ == '__main__':
    pass
