#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/7/31 下午3:23
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : shotgun.py
# @Software: PyCharm
from bootloader import config
from scrapy.http import Request
from scrapy.spider import Spider

__author__ = 'blackmatrix'


class AppleSpider(Spider):

    name = 'apple'
    allowed_domains = ['www.apple.com']
    start_urls = [
        'https://www.apple.com/cn/'
    ]
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': ' application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
        'Referer': 'https://www.apple.com/cn/'
    }

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.api_key = None
        self.login_url = None

    def start_requests(self):
        return [Request('https://www.apple.com/cn/', meta={'cookiejar': 1}, callback=self.prepare_login)]

    def prepare_login(self, resp):
        self.api_key = resp.selector.xpath(config['API_KEY_XPATH']).extract()[0]
        self.login_url = None
        pass

    def parse(self, response):
        pass


if __name__ == '__main__':
    pass
