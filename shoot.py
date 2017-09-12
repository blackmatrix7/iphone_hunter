#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 21:25
# @Author  : BlackMatrix
# @Site : 
# @File : shoot.py
# @Software: PyCharm
import os
import platform
from functools import partial
from selenium import webdriver
from config import current_config
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

__author__ = 'blackmatrix'


class AutoTest:

    def __init__(self):
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

    def wait_find_element_by_id(self, element_id, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=0.1
        ).until(lambda x: x.find_element_by_id(element_id))
        self.element_monkey_patch(element)
        return element

    def wait_find_element_by_xpath(self, xpath, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=0.1
        ).until(lambda x: x.find_element_by_xpath(xpath))
        self.element_monkey_patch(element)
        return element

    def wait_find_elements_by_xpath(self, xpath, parent=None):
        elements = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=0.1
        ).until(lambda x: x.find_elements_by_xpath(xpath))
        self.elements_monkey_patch(elements)
        return elements

    def wait_find_element_by_class_name(self, class_name, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=0.1
        ).until(lambda x: x.find_element_by_class_name(class_name))
        self.element_monkey_patch(element)
        return element

    def element_monkey_patch(self, element):
        for attr in dir(self):
            if attr.startswith('wait_'):
                setattr(element, attr, partial(getattr(self, attr), parent=element))

    def elements_monkey_patch(self, elements):
        try:
            iter(elements)
        except ValueError:
            elements = [elements]
        finally:
            for element in elements:
                self.element_monkey_patch(element)


class QuickBuy(AutoTest):

    def select_iphone(self, store):
        # 打开购买页面
        self.driver.get(current_config.TEST_URL)
        # 登录
        user = self.wait_find_element_by_id("username")
        user.send_keys(current_config.TEST_USER)
        password = self.wait_find_element_by_id("password")
        password.send_keys(current_config.TEST_PASS)
        login_btn = self.wait_find_element_by_class_name('logo-btn')
        login_btn.click()
        select_org = self.wait_find_element_by_xpath('//*[@id="layoutOrg"]')
        orgs = select_org.wait_find_elements_by_xpath('div[2]/div/div[2]/div/button')
        orgs[0].click()





if __name__ == '__main__':
    pass
