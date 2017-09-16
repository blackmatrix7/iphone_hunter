#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/9/15 下午2:43
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : courier.py
# @Software: PyCharm
from sms import SMSCenter
from extensions import rabbit

__author__ = 'blackmatrix'


# @rabbit.receive_from_rabbitmq(exchange_name='iphone', queue_name='sms', routing_key='apple')
def send_msg(message=None):
    """
    从消息队列获取需要发送的短信内容，发送成功并获取到验证码后，存储到缓存中
    :param message:
    :return:
    """
    client = SMSCenter()
    client.send_msg(targets=message['target'], content=message['content'])

    msg = client.get_msg()
    # TODO 解析短信文本，获取验证码
    # 将验证码写入缓存，20分钟超时
    cache.set('reg_code', msg, time=1200)
    return True

if __name__ == '__main__':
    pass
