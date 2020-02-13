# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ClassifiedWebCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    seller_name = scrapy.Field()
    seller_number = scrapy.Field()
    seller_email = scrapy.Field()
