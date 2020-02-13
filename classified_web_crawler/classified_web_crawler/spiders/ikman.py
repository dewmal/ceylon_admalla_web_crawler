# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from classified_web_crawler.classified_web_crawler.items import ClassifiedWebCrawlerItem


class IkmanSpider(CrawlSpider):
    name = 'ikman'
    allowed_domains = ['ikman.lk']
    start_urls = ['http://ikman.lk/']
    rules = (
        Rule(
            LinkExtractor(allow="^(http|https):\/\/ikman.lk\/(en|si)\/ad\/([^/]+)(^\/)?$"),
            callback="parse_item"
        ),
        Rule(
            LinkExtractor(allow="^(http|https)://ikman.lk/(en|si)/(ads|ad|shops|jobs).*."),
            callback='parse'
        ),
    )

    def parse_item(self, response):
        title = response.css(".item-top > h1:nth-child(1)::text").get()
        description = response.css("html body.on-item-detail div.app-content div.container.main div.ui-panel.is-rounded.item-detail div.ui-panel-content.ui-panel-block div.row.lg-g div.col-12.lg-8.item-body div.row.lg-g div.col-12.lg-8 div.item-description p::text").get()
        price = response.css("html body.on-item-detail div.app-content div.container.main div.ui-panel.is-rounded.item-detail div.ui-panel-content.ui-panel-block div.row.lg-g div.col-12.lg-8.item-body div.row.lg-g div.col-12.lg-8 div.item-price div.ui-price div.ui-price-tag span.amount::text").get()
        seller_name = response.css("html body.on-item-detail div.app-content div.container.main div.ui-panel.is-rounded.item-detail div.ui-panel-content.ui-panel-block div.row.lg-g div.item-top.col-12.lg-8 p.item-intro span.poster::text").get()
        location = response.css(".location::text").get()
        post_time = response.css(".location::text").get()

        item = ClassifiedWebCrawlerItem()
        item["title"] = title
        item["description"] = description
        item["price"] = price
        item["seller_name"] = seller_name
        item["location"] = location

        print(item.values())

        return item
