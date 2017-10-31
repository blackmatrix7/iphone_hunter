#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/9/15 下午12:17
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : huawei.py
# @Software: PyCharm
import gammu
import logging
from time import sleep
from config import current_config

__author__ = 'blackmatrix'


class SMSCenter:

    def __init__(self):
        self.state_machine = gammu.StateMachine()
        logging.info('[信使] 实例化完成')
        self.state_machine.ReadConfig(Filename=current_config['FILECONFIG'])
        logging.info('[信使] 读取短信设备配置完成')
        # Connect to the phone
        self.state_machine.Init()
        logging.info('[信使] 初始化完成')

    def send_msg(self, targets, content):
        message = {
            'Text': content,
            'SMSC': {'Location': 1},
            'Number': targets,
            'Coding': 'Unicode_No_Compression'
        }
        logging.info('[信使] 开始发送短信：{}'.format(message))
        self.state_machine.SendSMS(message)
        logging.info('[信使] 发送短信完成')

    def get_msg(self):
        location = 1
        while True:
            try:
                sms = self.state_machine.GetSMS(Folder=1, Location=location)
                logging.info('[信使] 收取短信完成：{}'.format(sms))
                if sms:
                    return sms
            except Exception as ex:
                logging.error('[信使] 短信收取失败，准备重试：{}'.format(ex))
                sleep(0.5)

    def del_msgs(self):
        """
        删除所有的短信
        """
        localtion = 1
        while True:
            try:
                self.state_machine.DeleteSMS(Folder=1, Location=localtion)
                logging.info('[信使] 删除所有短信')
                localtion += 1
            except Exception as ex:
                logging.error('[信使] 删除短信失败：{}'.format(ex))
                break


if __name__ == '__main__':
    pass

