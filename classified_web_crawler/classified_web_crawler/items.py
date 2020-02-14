# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ClassifiedWebCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    base_image = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    seller_name = scrapy.Field()
    seller_number = scrapy.Field()
    seller_email = scrapy.Field()
    metas = scrapy.Field()
    tags = scrapy.Field()
    raw_data = scrapy.Field()
    create_date = scrapy.Field()
    crawled_date = scrapy.Field()
    expire_date = scrapy.Field()
