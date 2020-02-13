# -*- coding: utf-8 -*-
import scrapy


class IkmanSpider(scrapy.Spider):
    name = 'ikman'
    allowed_domains = ['ikman.lk']
    start_urls = ['http://ikman.lk/']

    def parse(self, response):
        pass
