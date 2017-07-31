#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/7/31 下午3:23
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : shotgun.py
# @Software: PyCharm
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector

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

    def start_requests(self):
        return [Request('https://www.apple.com/cn/', meta={'cookiejar': 1}, callback=self.get_login_url)]

    @staticmethod
    def get_login_url(resp):
        selector = Selector(resp)
        url = selector.xpath('//*[@id="ac-gn-bagview-content"]').extract()

    def parse(self, response):
        pass


if __name__ == '__main__':
    pass
