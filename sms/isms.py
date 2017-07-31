#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/7/31 上午10:21
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : isms.py
# @Software: PyCharm
from abc import ABCMeta, abstractmethod
__author__ = 'blackmatrix'


class ISMSCenter(metaclass=ABCMeta):

    @abstractmethod
    def send_msg(self, targets, content):
        raise NotImplementedError

    @abstractmethod
    def get_msg(self):
        raise NotImplementedError


if __name__ == '__main__':
    pass
