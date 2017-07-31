#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/7/31 下午10:19
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: config
# @Software: PyCharm

__author__ = 'blackmatrix'


class BaseConfig:

    API_KEY_XPATH = '//*[@name="ac-gn-store-key"]/@content'

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

if __name__ == '__main__':
    pass
