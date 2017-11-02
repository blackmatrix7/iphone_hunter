#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/9/15 下午2:43
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : courier.py
# @Software: PyCharm
import json
import logging
from sms import SMSCenter
from config import current_config
from extensions import rabbit, cache

__author__ = 'blackmatrix'


client = SMSCenter()


@rabbit.receive_from_rabbitmq(exchange_name='iphone', queue_name='sms', routing_key='apple')
def send_msg(message=None):
    """
    从消息队列获取需要发送的短信内容，发送成功并获取到验证码后，存储到缓存中
    :param message:
    :return:
    """
    message = json.loads(message)
    logging.info('[信使] 接收到需要验证的短信')

    # 发送短信前，删除所有的短信
    client.del_msgs()
    logging.info('[信使] 发送短信前，删除所有短信')
    client.send_msg(targets=message['target'], content=message['content'])
    logging.info('[信使] 验证短信已发送')

    # 获取短信
    sms_list = [
        {
            'datetime': sms['DateTime'],
            'text': sms['Text'],
            'send_from': current_config.PHONE_NUMBER
        }
        for sms in client.get_msg()
    ]
    logging.info('[信使] 已收到短信：{}'.format(sms_list))

    # 将验证码写入缓存，30分钟超时
    cache.set(message['apple_id'], sms_list, time=1750)
    logging.info('[信使] 将短信写入缓存：{}'.format(sms_list))
    # 发送短信后，再次清理所有短信
    client.del_msgs()
    logging.info('[信使] 发送短信后，删除所有短信')
    # 临时加入一个延迟的方法，避免一个号码连续发送两次
    from time import sleep
    sleep(30)
    return True


if __name__ == '__main__':
    pass
