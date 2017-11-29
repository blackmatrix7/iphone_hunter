#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 21:25
# @Author  : BlackMatrix
# @Site : 
# @File : shoot.py
# @Software: PyCharm
import json
import logging
import platform
from time import sleep
from toolkit import retry
from functools import partial
from selenium import webdriver
from operator import itemgetter
from config import current_config
from extensions import rabbit, cache
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.ui import Select as DefaultSelect

__author__ = 'blackmatrix'

custom_retry = partial(retry, max_retries=30, step=0.2)


class ErrorBuy(Exception):
    pass


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
            setattr(element, attr, custom_retry()(getattr(element, attr)))

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

    def is_elements_by_xpath(self, xpath):
        """
        判断元素是否存在，有个2秒的延迟。
        :param xpath:
        :return:
        """
        try:
            WebDriverWait(
                driver=self.driver,
                timeout=1,
                poll_frequency=current_config['POLL_FREQUENCY']
            ).until(lambda x: x.find_elements_by_xpath(xpath))
            return True
        except ElementNotVisibleException:
            return False


class Select(DefaultSelect):

    def __init__(self, webelement):
        super().__init__(webelement)

    def select_by_index(self, index):
        return custom_retry()(super(Select, self).select_by_index)(index)

    def select_by_value(self, value):
        return custom_retry()(super(Select, self).select_by_value)(value)

    def select_by_visible_text(self, text):
        return custom_retry()(super(Select, self).select_by_visible_text)(text)

    def deselect_all(self):
        return custom_retry()(super().deselect_all)()

    def deselect_by_value(self, value):
        return custom_retry()(super().deselect_by_value)(value)

    def deselect_by_index(self, index):
        return custom_retry()(super().deselect_by_index)(index)

    def deselect_by_visible_text(self, text):
        return custom_retry()(super().deselect_by_visible_text)(text)


class Shoot(AutoTest):

    def __init__(self):
        self.model = None
        self.color = None
        self.space = None
        self.store = None
        self.first_name = None
        self.last_name = None
        self.idcard = None
        self.quantity = None
        self.apple_id = None
        self.apple_id_pass = None
        self.email = current_config.EMAIL
        self.send_message = partial(rabbit.send_message, exchange_name='iphone', queue_name='sms')
        super().__init__()

    @retry(max_retries=5, delay=1, callback=logging.error)
    def select_iphone(self, model, color, space, store,
                      first_name, last_name, idcard, quantity,
                      apple_id, apple_id_pass, email):
        self.model = model
        self.color = color
        self.space = space
        self.store = store
        self.first_name = first_name
        self.last_name = last_name
        self.idcard = idcard
        self.quantity = quantity
        self.apple_id = apple_id
        self.email = email
        self.apple_id_pass = apple_id_pass
        # 打开购买页面
        logging.info('[猎手] 正在打开购买页面')
        self.driver.get(current_config.get_buy_url(model=model, color=color, space=space))
        logging.info('[猎手] 当前链接：{}'.format(self.driver.current_url))
        logging.info('[猎手] 已打开购买页面')
        # 数量
        select_quantity = Select(self.wait_find_element_by_xpath(current_config.SELECT_QUANTITY))
        select_quantity.select_by_value(str(quantity))
        logging.info('[猎手] 已选择数量{}'.format(quantity))
        # 零售店
        select_store = Select(self.wait_find_element_by_xpath(current_config['SELECT_STORE']))
        select_store.select_by_value(store)
        logging.info('[猎手] 已选择零售店{}'.format(store))

        # 继续
        btn_to_login = self.wait_find_element_by_xpath(current_config['BTN_TO_LOGIN'])
        btn_to_login.click()
        logging.info('[猎手] 点击继续按钮，跳转到下一页')
        if self.driver.current_url == 'https://www.apple.com/cn/iphone/':
            # 说明预约失败
            return True
        elif 'signin.apple.com' in self.driver.current_url:
            # 需要登录
            self.login_apple_id()
        else:
            # 已经登录
            self.send_reg_code()

    @retry(max_retries=5, delay=1)
    def login_apple_id(self):
        logging.info('[猎手] 当前链接：{}'.format(self.driver.current_url))
        # 切换到iframe
        logging.info('[猎手] 准备登录Apple Id')
        iframe = self.wait_find_element_by_xpath('//*[@id="aid-auth-widget-iFrame"]')
        self.driver.switch_to.frame(iframe)
        # 帐号
        input_apple_id = self.wait_find_element_by_xpath(current_config.APPLE_ID_XPATH)
        input_apple_id.send_keys(self.apple_id)
        logging.info('[猎手] 输入Apple Id 帐号')
        # 密码
        input_apple_pwd = self.wait_find_element_by_xpath(current_config.APPLE_PASS_XPATH)
        input_apple_pwd.send_keys(self.apple_id_pass)
        logging.info('[猎手] 输入Apple Id 密码')
        # 登录
        btn_login = self.wait_find_element_by_xpath(current_config.APPLE_LOGIN_XPATH)
        btn_login.click()
        logging.info('[猎手] 点击登录按钮')
        self.send_reg_code()
        logging.info('[猎手] 准备跳转短信验证页面')

    @retry(max_retries=5, delay=1)
    def send_reg_code(self):
        """
        申请注册码
        :return:
        """
        logging.info('[猎手] 当前链接：{}'.format(self.driver.current_url))
        # 注册码，暂时没什么用，最终是通过缓存获取到用于验证的注册码
        reg_code = '123456'
        # 手机号，暂时没什么用，最终是通过缓存获取到用于验证的手机号码
        phone_number = '18858888888'

        # 获取页面元素
        validate_reg_code = self.wait_find_element_by_xpath(current_config.VALIDATE_REG_CODE)
        btn_continue = current_config.BTN_NEED_REG_CODE_XPATH

        # 需要申请注册码的情况
        if validate_reg_code.text == '申请并验证你的注册码。':
            # 说明验证码已经过期，清理掉
            cache.delete(self.apple_id)
            # 重新申请一个
            logging.info('[猎手] 需要申请注册码')
            btn_continue = current_config.BTN_NEED_SEND_SMS_XPATH
            # 验证码
            sms_code = self.wait_find_element_by_xpath(current_config.SMS_CODE_XPATH)
            logging.info('[猎手] 页面验证码为{}'.format(sms_code.text))
            # 发送短信
            rabbit.connect()
            self.send_message(messages={'content': sms_code.text,
                                        'target': current_config.SEND_TO,
                                        'apple_id': self.apple_id})
            logging.info('[猎手] 将验证码发送给消息队列')
            rabbit.disconnect()

        # 遍历获取缓存注册码
        logging.info('[猎手] 等待获取注册码短信')
        while True:
            sms_list = cache.get(self.apple_id)
            if sms_list:
                logging.info('[猎手] 已获取到短信：{}'.format(sms_list))
                break

        # 排序
        sms_list.sort(key=itemgetter('datetime'))
        for sms in sms_list:
            if '注册码' in sms['text']:
                phone_number = sms['send_from']
                reg_code = sms['text'][6:15]
                logging.info('[猎手] 解析短信完成，apple id：{0}，注册码：{1}'.format(self.apple_id, reg_code))
                break

        # 填写手机号码
        input_phone_number = self.wait_find_element_by_xpath(current_config.PHONE_NUMBER_XPATH)
        input_phone_number.clear()
        input_phone_number.send_keys(phone_number)
        logging.info('[猎手] 已填写手机号码：{}'.format(phone_number))

        # 填写注册码
        input_reg_code = self.wait_find_element_by_xpath(current_config.REG_CODE_XPATH)
        input_reg_code.clear()
        input_reg_code.send_keys(reg_code)
        logging.info('[猎手] 已填写注册码：{}'.format(reg_code))

        # 继续
        btn_continue = self.wait_find_element_by_xpath(btn_continue)
        sleep(1)
        btn_continue.click()
        logging.info('[猎手] 点击继续按钮')
        # 如果出现注册码错误，清理缓存并重试
        # if self.is_elements_by_xpath(current_config.ERR_REG_CODE):
        #     err_reg_code = self.wait_find_element_by_xpath(current_config.ERR_REG_CODE)
        #     if err_reg_code.is_displayed() is True:
        #         cache.delete(current_config.APPLE_ID)
        #         raise ErrorBuy
        logging.info('[猎手] 准备进行最后一步预约')
        self.last_step()

    @retry(max_retries=5, delay=1)
    def last_step(self):
        logging.info('[猎手] 当前链接：{}'.format(self.driver.current_url))
        # 选择预约时间段，默认选择最晚，这样可以最大程度保证及时赶到Apple Store
        select_time = Select(self.wait_find_element_by_xpath(current_config.SELECT_TIME_XPATH))
        select_time.select_by_visible_text('下午 8:00 - 下午 8:30')
        logging.info('[猎手] 选择预约时间段：下午 8:00 - 下午 8:30')

        # 输入姓
        input_last_name = self.wait_find_element_by_xpath(current_config.LAST_NAME_XPATH)
        input_last_name.clear()
        input_last_name.send_keys(self.last_name)
        logging.info('[猎手] 已输入姓：{}'.format(self.last_name))

        # 输入名
        input_first_name = self.wait_find_element_by_xpath(current_config.FIRST_NAME_XPATH)
        input_first_name.clear()
        input_first_name.send_keys(self.first_name)
        logging.info('[猎手] 已输入名：{}'.format(self.first_name))

        # 输入电子邮箱，支持为每个购买者配置单独的邮箱
        input_email = self.wait_find_element_by_xpath(current_config.EMAIL_XPATH)
        input_email.clear()
        input_email.send_keys(self.email)
        logging.info('[猎手] 已输入邮箱：{}'.format(self.email))

        # 输入证件信息
        select_idcard = Select(self.wait_find_element_by_xpath(current_config.GOV_ID_TYPE_XPATH))
        select_idcard.select_by_value('idCardChina')
        input_idcard = self.wait_find_element_by_xpath(current_config.GOV_ID_XPATH)
        input_idcard.clear()
        input_idcard.send_keys(self.idcard)
        logging.info('[猎手] 已输入证件信息：{}'.format(self.idcard))

        # 点击预约按钮
        btn_buy = self.wait_find_element_by_xpath(current_config.BTN_BUY_XPATH)
        btn_buy.click()
        logging.info('[猎手] 已点击预约按钮')

        # 暂定休眠60秒后，关闭浏览器
        sleep(60)
        self.driver.close()


def quick_buy(message):
    try:
        # 为每个进程单独打开一个浏览器
        shoot = Shoot()
        # 测试数据
        # message = {'model': 'iPhone X', 'color': '深空灰色', 'space': '256GB', 'store': 'R600',
        #            'first_name': '三', 'last_name': '李', 'idcard': 123122222, 'quantity': 1}
        logging.info('[猎手] 进程启动，购买信息：{}'.format(message))
        shoot.select_iphone(model=message['model'], color=message['color'],
                            space=message['space'], store=message['store'],
                            first_name=message['first_name'], last_name=message['last_name'],
                            idcard=message['idcard'], quantity=message['quantity'],
                            apple_id=message['apple_id'], apple_id_pass=message['apple_id_pass'],
                            email=message['email'])
    except Exception as ex:
        logging.error(ex)
        return True


def hunting():

    # 为每个进程单独打开一个浏览器
    shoot = Shoot()

    @retry(max_retries=5, delay=1)
    # 从消息队列获取订购信息，如果
    @rabbit.receive_from_rabbitmq(exchange_name='iphone', queue_name='buyers', routing_key='apple')
    def start(message=None):
        try:
            message = json.loads(message.decode())
            # 测试数据
            # message = {'model': 'iPhone X', 'color': '深空灰色', 'space': '256GB', 'store': 'R600',
            #            'first_name': '三', 'last_name': '李', 'idcard': 123122222, 'quantity': 1}
            logging.info('[猎手] 进程启动，购买信息：{}'.format(message))
            shoot.select_iphone(model=message['model'], color=message['color'],
                                space=message['space'], store=message['store'],
                                first_name=message['first_name'], last_name=message['last_name'],
                                idcard=message['idcard'], quantity=message['quantity'],
                                apple_id=message['apple_id'], apple_id_pass=message['apple_id_pass'],
                                email=message['email'])
        except Exception as ex:
            logging.error('[猎手] {}'.format(ex))
            return True

    start()


if __name__ == '__main__':
    pass
