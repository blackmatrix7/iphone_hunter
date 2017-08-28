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
from urllib.parse import urlsplit
from bootloader import config
from scrapy.http import Request, FormRequest

__author__ = 'blackmatrix'


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

    def start_requests(self):
        yield Request(config['APPLE_INDEX'], meta={'cookiejar': 1}, callback=self.get_api_key)

    def get_api_key(self, resp):
        self.api_key = resp.selector.xpath(config['API_KEY_XPATH']).extract()[0]
        yield Request(config['APPLE_FLYOUT_AJAX'].format(self.api_key), callback=self.get_login_url)

    def get_login_url(self, resp):
        resp_json = json.loads(resp.body.decode('utf-8'))
        for item in resp_json.get('links', []):
            if item.get('type') == 'signIn':
                self.login_url = item['url']
                break
        yield Request(self.login_url, callback=self.login_appleid)

    def login_appleid(self, resp):
        """
        模拟登录
        :param resp:
        :return:
        """
        url = urllib.parse.urlparse(resp.url)
        query = urllib.parse.parse_qs(resp.url)
        yield FormRequest(config.APPLE_SING_IN.format(url.hostname),
                          formdata={'login-appleId': config.get('APPLE_ID'),
                                    'login-password': config.get('APPLE_ID_PASS'),
                                    '_a': 'login.sign',
                                    '_fid': 'si',
                                    'r': query['r'][0],
                                    's': query['s'][0],
                                    'c': query['s'][0]},
                          method='POST',
                          callback=self.test_login)

    def test_login(self, resp):
        """
        TODO 保持登录状态
        :param resp:
        :return:
        """
        body = resp.body.decode('utf-8')
        print(body)

    def parse(self, response):
        pass


if __name__ == '__main__':
    pass