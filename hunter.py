#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 21:25
# @Author  : BlackMatrix
# @Site : 
# @File : shoot.py
# @Software: PyCharm
import platform
from functools import partial
from selenium import webdriver
from config import current_config
from extensions import rabbit, cache
from tookit import retry as default_retry
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.ui import Select as DefaultSelect

__author__ = 'blackmatrix'

retry = partial(default_retry, max_retries=30, step=0.2)


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
        self.driver.set_window_size(1440, 900)

    def element_monkey_patch(self, element):

        for attr in dir(self):
            if attr.startswith('wait_'):
                setattr(element, attr, partial(getattr(self, attr), parent=element))
        # 针对dom元素的部分操作，加入重试方法
        for attr in ('click', 'submit', 'clear', 'send_keys'):
            setattr(element, attr, retry()(getattr(element, attr)))

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
            poll_frequency=current_config['POLL_FREQUENCY']
        ).until(lambda x: x.find_element_by_id(element_id))
        self.element_monkey_patch(element)
        return element

    def wait_find_element_by_xpath(self, xpath, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=current_config['POLL_FREQUENCY']
        ).until(lambda x: x.find_element_by_xpath(xpath))
        self.element_monkey_patch(element)
        return element

    def wait_find_element_by_class_name(self, class_name, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=current_config['POLL_FREQUENCY']
        ).until(lambda x: x.find_element_by_class_name(class_name))
        self.element_monkey_patch(element)
        return element

    def wait_find_element_by_link_text(self, link_text, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=current_config['POLL_FREQUENCY']
        ).until(lambda x: x.find_element_by_link_text(link_text))
        self.element_monkey_patch(element)
        return element

    def wait_find_element_by_name(self, name, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=current_config['POLL_FREQUENCY']
        ).until(lambda x: x.find_element_by_name(name))
        self.element_monkey_patch(element)
        return element

    def wait_find_elements_by_xpath(self, xpath, parent=None):
        elements = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=current_config['POLL_FREQUENCY']
        ).until(lambda x: x.find_elements_by_xpath(xpath))
        self.elements_monkey_patch(elements)
        return elements


class Select(DefaultSelect):

    def __init__(self, webelement):
        super().__init__(webelement)

    def select_by_index(self, index):
        return retry()(super(Select, self).select_by_index)(index)

    def select_by_value(self, value):
        return retry()(super(Select, self).select_by_value)(value)

    def select_by_visible_text(self, text):
        return retry()(super(Select, self).select_by_visible_text)(text)

    def deselect_all(self):
        return retry()(super().deselect_all)()

    def deselect_by_value(self, value):
        return retry()(super().deselect_by_value)(value)

    def deselect_by_index(self, index):
        return retry()(super().deselect_by_index)(index)

    def deselect_by_visible_text(self, text):
        return retry()(super().deselect_by_visible_text)(text)


class Shoot(AutoTest):

    def __init__(self):
        self.send_message = partial(rabbit.send_message, exchange_name='iphone', queue_name='sms')
        super().__init__()

    def select_iphone(self, model, color, space, store, first_name, last_name, idcard, quantity):
        # 打开购买页面
        self.driver.get(current_config.get_buy_url(model=model, color=color, space=space))
        # 数量
        select_quantity = Select(self.wait_find_element_by_xpath(current_config.SELECT_QUANTITY))
        select_quantity.select_by_value(str(quantity))
        # 零售店
        select_store = Select(self.wait_find_element_by_xpath(current_config['SELECT_STORE']))
        select_store.select_by_value(store)
        # 继续
        btn_to_login = self.wait_find_element_by_xpath(current_config['BTN_TO_LOGIN'])
        btn_to_login.click()

    def login_apple_id(self):
        # 如果无需登录则直接购买
        if 'signin.apple.com' not in self.driver.current_url:
            self.send_reg_code()
        else:
            # 切换到iframe
            iframe = self.wait_find_element_by_xpath('//*[@id="aid-auth-widget-iFrame"]')
            self.driver.switch_to.frame(iframe)
            # 帐号
            input_apple_id = self.wait_find_element_by_xpath(current_config.APPLE_ID_XPATH)
            input_apple_id.send_keys(current_config.APPLE_ID)
            # 密码
            input_apple_pwd = self.wait_find_element_by_xpath(current_config.APPLE_PASS_XPATH)
            input_apple_pwd.send_keys(current_config.APPLE_ID_PASS)
            # 登录
            btn_login = self.wait_find_element_by_xpath(current_config.APPLE_LOGIN_XPATH)
            btn_login.click()
            self.send_reg_code()

    def send_reg_code(self):
        """
        申请注册码
        :return:
        """
        # 接收到的短信
        sms_code = self.wait_find_element_by_xpath(current_config.SMS_CODE_XPATH)
        rabbit.connect()
        self.send_message(messages={'content': sms_code.text, 'send_to': current_config.SEND_TO})
        rabbit.disconnect()
        input_phone_number = self.wait_find_element_by_xpath(current_config.PHONE_NUMBER_XPATH)
        input_phone_number.send_keys(current_config.PHONE_NUMBER)
        # 遍历获取缓存验证码
        while True:
            sms = cache.get('reg_code')
            if sms is not None:
                break
        reg_code = sms

        input_reg_code = self.wait_find_element_by_xpath(current_config.REG_CODE_XPATH)
        input_reg_code.send_keys(reg_code)

        print(reg_code)


def hunting():

    # 为每个进程单独打开一个浏览器
    shoot = Shoot()

    # 从消息队列获取订购信息，如果
    # @rabbit.receive_from_rabbitmq(exchange_name='iphone', queue_name='stock', routing_key='apple')
    def start():
        shoot.select_iphone(model='iPhone 8', color='深空灰色', space='64GB', store='R581',
                            first_name='三', last_name='张', idcard='123456789', quantity=2)
        shoot.login_apple_id()
        # apple_stores = falcon.get_apple_stores()
        # iphone_stock = falcon.search_iphone()
        # for watch_store_key, watch_store_value in iphone_stock.items():
        #     # TODO 判断库存是否有需要购买的型号
        #     pass
        # quick_buy.select_iphone('R607')
    start()


if __name__ == '__main__':
    pass
