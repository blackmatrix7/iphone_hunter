#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 21:25
# @Author  : BlackMatrix
# @Site : 
# @File : shoot.py
# @Software: PyCharm
import os
import platform
from tookit import retry
from functools import partial
from selenium import webdriver
from config import current_config
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException

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
        self.driver.set_window_size(1024, 768)

    def element_monkey_patch(self, element):
        for attr in dir(self):
            if attr.startswith('wait_'):
                setattr(element, attr, partial(getattr(self, attr), parent=element))
        # 针对dom元素的部分操作，加入重试方法
        for attr in ('click', 'submit', 'clear', 'send_keys'):
            setattr(element, attr, retry(max_retries=10, step=0.5)(getattr(element, attr)))

    def elements_monkey_patch(self, elements):
        try:
            iter(elements)
        except ValueError:
            elements = [elements]
        finally:
            for element in elements:
                self.element_monkey_patch(element)

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

    def wait_find_element_by_class_name(self, class_name, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=0.1
        ).until(lambda x: x.find_element_by_class_name(class_name))
        self.element_monkey_patch(element)
        return element

    def wait_find_element_by_link_text(self, link_text, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=0.1
        ).until(lambda x: x.find_element_by_link_text(link_text))
        self.element_monkey_patch(element)
        return element

    def wait_find_element_by_name(self, name, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=0.1
        ).until(lambda x: x.find_element_by_name(name))
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
        self.wait_find_element_by_link_text('客户档案管理').click()
        self.wait_find_element_by_xpath('/html/body/div[3]/div[1]/div/div/div/ul/li[3]/ul/li[2]/a[2]').click()
        add_customer_btn = self.wait_find_element_by_xpath('//*[@id="msview"]/div/div/div[1]/div[2]/a')
        add_customer_btn.click()
        self.wait_find_element_by_name('archiveName').send_keys('他二舅')
        Select(self.wait_find_element_by_name("archiveGender")).select_by_value('1')
        Select(self.wait_find_element_by_name("archiveCustomerSource")).select_by_index(1)
        Select(self.wait_find_element_by_name("CustomerQue")).select_by_index(1)
        self.wait_find_element_by_xpath('//*[@id="baseInfoBox"]/div[1]/div[1]/div[8]/div[2]/a').click()
        # self.driver.quit()

if __name__ == '__main__':
    pass
