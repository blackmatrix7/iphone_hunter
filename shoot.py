#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 21:25
# @Author  : BlackMatrix
# @Site : 
# @File : shoot.py
# @Software: PyCharm
import os
import platform
from selenium import webdriver
from config import current_config
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

__author__ = 'blackmatrix'


class QuickBuy:

    def __init__(self):
        path = current_config.PROJ_PATH
        # 初始化浏览器
        options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        if platform.system() == 'Darwin':
            executable_path = '{0}/{1}'.format(current_config.PROJ_PATH, 'chromedriver')
        else:
            executable_path = 'chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=options)
        self.driver.implicitly_wait(current_config['TIME_OUT'])

    def find_element_by_id(self, element_id):
        element = Select(
            WebDriverWait(
                driver=self.driver,
                timeout=current_config['TIME_OUT'],
                poll_frequency=0.1
            ).until(lambda x: x.find_element_by_id(element_id)))
        return element

    def find_element_by_xpath(self, xpath):
        element = Select(
            WebDriverWait(
                driver=self.driver,
                timeout=current_config['TIME_OUT'],
                poll_frequency=0.1
            ).until(lambda x: x.find_element_by_xpath(xpath)))
        return element

    def select_iphone(self, store):
        # 打开购买页面
        self.driver.get('http://www.cnbeta.com')
        # 选择零售店
        select_store = self.find_element_by_id('selectStore')
        select_store.select_by_value(store)
        # 选择机型
        select_subfamily = self.find_element_by_id('selectSubfamily')


if __name__ == '__main__':
    pass
