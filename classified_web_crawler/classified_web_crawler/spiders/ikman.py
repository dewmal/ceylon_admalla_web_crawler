# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor


class IkmanSpider(scrapy.Spider):
    name = 'ikman'
    allowed_domains = ['ikman.lk']
    start_urls = ['http://ikman.lk/']

    def parse(self, response):
        page = response.url.split("/")[-2]

        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)

        # next_urls = response.css('a').xpath('@href').getall()
        # if next_urls:
        #     for next_url in next_urls:
        #         pass
        #
        #     next_page = ""

        for link in links:
            next_page = link.url
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
