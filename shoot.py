#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 21:25
# @Author  : BlackMatrix
# @Site : 
# @File : shoot.py
# @Software: PyCharm
from selenium import webdriver
from config import current_config
__author__ = 'blackmatrix'


class QuickBuy:

    def __init__(self):
        options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(executable_path=r"chromedriver.exe", chrome_options=options)
        self.driver.implicitly_wait(current_config['TIME_OUT'])

    def select_iphone(self):
        self.driver.get('https://reserve-cn.apple.com/CN/zh_CN/reserve/iPhone/availability?channel=1')
        # yield

if __name__ == '__main__':
    pass
