# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import scrapy
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule

from scrapy.linkextractors import LinkExtractor

from classified_web_crawler.classified_web_crawler.items import ClassifiedWebCrawlerItem


class HitadSpider(CrawlSpider):
    name = 'hitad'
    allowed_domains = ['hitad.lk']
    start_urls = ['http://hitad.lk/']

    # crawler_url_rule: str = "^(http|https)://www.hitad.lk/(en|si)/(ads|ad|shops|jobs).*."
    # data_extract_rule: str = "^(http|https):\/\/www.hitad.lk\/(en|si)\/ad\/([^/]+)(^\/)?$"

    rules = (
        Rule(
            LinkExtractor(allow="^(http|https):\/\/www.hitad.lk\/(en|si)\/ad\/([^/]+)(^\/)?$"),
            callback="parse_item"
        ),
        Rule(
            LinkExtractor(allow="^(http|https)://www.hitad.lk/(en|si)/(ads|ad|shops|jobs).*."),
            callback='parse'
        ),
    )

    def parse_item(self, response):
        self.parse(response)

        base_image = response.css(
            "div.product-img img.img-fluid").xpath('@src').get()

        title = response.css("meta[property='og:title']").xpath("@content").get()
        content = response.css("meta[property='og:description']").xpath("@content").get()
        post_date = response.css("meta[itemprop='datePublished']").xpath("@content").get()
        expire_date = datetime.strptime(post_date, "%Y-%m-%d %H:%M %p")
        expire_date = expire_date + timedelta(days=14)

        soup = BeautifulSoup(response.body, 'html.parser')

        _content = soup.select("div.ads-details-info p")
        _content = ' '.join([_c.text.strip() for _c in _content])
        content = f"{content}, {_content}"

        # Person Name
        person_name = 'Seller'
        # Contact Details
        contact_numbers = soup.select('h3.ph-cont a')
        contact_numbers = [c.text.strip() for c in contact_numbers]

        # Location
        locations = soup.select('ol.breadcrumb li.breadcrumb-item a')
        locations = [l.text.strip() for l in [locations[1], locations[2]]]

        # Tags
        tags = soup.select('ol.breadcrumb li.breadcrumb-item a')
        tags = [t.text.strip() for t in tags]

        # Keys
        metas_ = soup.select('div.agent-inner h4')
        metas = {}
        for m in metas_:
            # print(m.text)
            key = m.select('strong')
            # print(key)
            key = key[0].text.strip() if key and len(key) > 0 else ''
            value = m.select('span')
            # print(value)
            value = value[0].text.strip() if value and len(value) > 0 else ''
            #
            metas[key] = value

        item = ClassifiedWebCrawlerItem()
        item["crawler_name"] = self.name
        item["url"] = response.url
        item["base_image"] = base_image
        item["title"] = title
        item["description"] = content
        item["price"] = 0
        item["seller_name"] = person_name
        item["seller_number"] = contact_numbers
        item["location"] = locations
        item["tags"] = tags
        item["metas"] = metas
        item["raw_data"] = soup.text
        item["create_date"] = post_date
        item["expire_date"] = expire_date
        item["crawled_date"] = datetime.now()

        yield item
