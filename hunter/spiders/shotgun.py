#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/7/31 下午3:23
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : shotgun.py
# @Software: PyCharm
import re
import json
import scrapy
import urllib
import base64
import requests
from lxml import etree
from urllib.parse import urlsplit
from config import current_config
from scrapy.http import Request, FormRequest

__author__ = 'blackmatrix'
#
#
# class AppleSpider:
#
#     def __init__(self):
#         self.site_map = None
#         self.session = None
#         self.cookies = None
#         self.api_key = None
#         self.headers = {'Accept': '*/*',
#                         'Accept-Encoding': 'gzip,deflate',
#                         'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4',
#                         'Connection': 'keep-alive',
#                         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#                         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
#                                   'AppleWebKit/537.36 (KHTML, like Gecko) '
#                                   'Chrome/38.0.2125.111 Safari/537.36',
#                         'Referer': 'https://www.apple.com/cn/'}
#
#     def shoot(self):
#         self.session = requests.session()
#         api_key = self.get_api_key()
#         login_url = self.get_login_url(api_key)
#         self.login_appleid(login_url)
#         self.get_my_orders()
#
#     def get_api_key(self):
#         resp = self.session.get(current_config['APPLE_INDEX'])
#         html = resp.content
#         selector = etree.HTML(html)
#         self.api_key = selector.xpath(current_config['API_KEY_XPATH'])[0]
#         return self.api_key
#
#     def get_login_url(self, api_key=None):
#         api_key = api_key or self.api_key
#         resp = self.session.get(current_config['APPLE_FLYOUT_AJAX'].format(api_key))
#         site_urls = resp.json()
#         self.site_map = {}
#         for url in site_urls['links']:
#             self.site_map[url['type']] = url['url']
#         return self.site_map['signIn']
#
#     def login_appleid(self, login_url):
#         query = urllib.parse.parse_qs(login_url)
#         url = urllib.parse.urlparse(login_url)
#         resp = self.session.post(current_config.APPLE_SING_IN.format(url.hostname),
#                                  data={'login-appleId': current_config.get('APPLE_ID'),
#                                        'login-password': current_config.get('APPLE_ID_PASS'),
#                                        '_a': 'login.sign',
#                                        '_fid': 'si',
#                                        'r': query['r'][0],
#                                        's': query['s'][0],
#                                        'c': query['s'][0]})
#         self.cookies = resp.cookies
#         pass
#
#     def get_my_orders(self):
#         orders_url = 'https://secure2.store.apple.com/cn/order/list'
#         resp = self.session.get(orders_url, headers=self.headers, cookies=self.cookies)
#         if '打印所有电子收据' in resp.text:
#             pass
#         return resp


class AppleSpider(scrapy.spiders.Spider):

    name = 'apple'
    allowed_domains = ['apple.com']
    start_urls = [
        'https://www.apple.com/cn/'
    ]
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': ' application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/38.0.2125.111 Safari/537.36',
        'Referer': 'https://www.apple.com/cn/'
    }

    def __init__(self, name=None, **kwargs):

        super().__init__(name=name, **kwargs)
        self.api_key = None
        self.login_url = None
        self.site_map = {}

    def start_requests(self):
        yield Request(current_config['APPLE_INDEX'], meta={'cookiejar': 1}, callback=self.get_api_key)

    def get_api_key(self, resp):
        self.api_key = resp.selector.xpath(current_config['API_KEY_XPATH']).extract()[0]
        yield Request(current_config['APPLE_FLYOUT_AJAX'].format(self.api_key), callback=self.get_login_url, meta={'cookiejar': resp.meta['cookiejar']})

    def get_login_url(self, resp):
        urls = json.loads(resp.body.decode('utf-8'))
        for url in urls['links']:
            self.site_map[url['type']] = url['url']
        yield Request(self.site_map['signIn'], callback=self.login_appleid, meta={'cookiejar': resp.meta['cookiejar']})

    def login_appleid(self, resp):
        """
        模拟登录
        :param resp:
        :return:
        """
        url = urllib.parse.urlparse(resp.url)
        query = urllib.parse.parse_qs(resp.url)
        yield FormRequest(current_config.APPLE_SING_IN.format(url.hostname),
                          formdata={'login-appleId': current_config.get('APPLE_ID'),
                                    'login-password': current_config.get('APPLE_ID_PASS'),
                                    '_a': 'login.sign',
                                    '_fid': 'si',
                                    'r': query['r'][0],
                                    's': query['s'][0],
                                    'c': query['s'][0]},
                          method='POST',
                          meta={'cookiejar': resp.meta['cookiejar']},
                          callback=self.login_success)

    def login_success(self, resp):
        url = self.site_map['orders']
        yield Request.F(url, callback=self.redirect_store, meta={'cookiejar': resp.meta['cookiejar']})

    def redirect_store(self, resp):
        if '打印所有电子收据' in resp.text:
            pass
        print(resp)

    def parse(self, response):
        pass


if __name__ == '__main__':
    pass
