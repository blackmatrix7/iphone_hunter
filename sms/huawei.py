#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/9/15 下午12:17
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : huawei.py
# @Software: PyCharm
import gammu
from time import sleep
from .isms import ISMSCenter
from config import current_config

__author__ = 'blackmatrix'


class SMSCenter(ISMSCenter):

    def __init__(self):
        self.state_machine = gammu.StateMachine()
        self.state_machine.ReadConfig(Filename=current_config['FILECONFIG'])
        # Connect to the phone
        self.state_machine.Init()

    def send_msg(self, targets, content):
        message = {
            'Text': content,
            'SMSC': {'Location': 1},
            'Number': targets,
            'Coding': 'Unicode_No_Compression'
        }
        self.state_machine.SendSMS(message)

    def get_msg(self):
        location = 1
        while True:
            try:
                sms = self.state_machine.GetSMS(Folder=1, Location=location)
                if sms:
                    return sms
            except Exception as ex:
                print(ex)
                sleep(0.5)

    def del_msgs(self):
        """
        删除所有的短信
        """
        localtion = 1
        while True:
            try:
                self.state_machine.DeleteSMS(Folder=1, Location=localtion)
                localtion += 1
            except Exception as ex:
                print(ex)
                break



        # a = self.state_machine.GetSMS(Folder=1, Location=1)
        # self.state_machine.SMS
        # self.state_machine.DeleteSMS(Folder=1, Location=1)
        # b = self.state_machine.GetSMSFolders()
        # print(a)


if __name__ == '__main__':
    pass
