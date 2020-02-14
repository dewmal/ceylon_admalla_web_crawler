# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from selenium import webdriver

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

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        # import chromedriver_binary
        import chromedriver_binary

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def parse_item(self, response):
        self.driver.get(response.url)
        all_show_number = self.driver.find_element_by_css_selector("span.gtm-show-number")
        all_show_number.click()

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        title = soup.select("title")[0]
        title = title.text if title else ''
        # Content
        content = soup.select("div.item-description")[0]
        content = content.text if content else ''
        # Person Name
        person_name = soup.select("span.poster")[0]
        person_name = person_name.text if person_name else ''
        # Contact Details
        contact_numbers = soup.select('.item-contact-more.is-showable ul:first-child span.h3')
        contact_numbers = [c.text for c in contact_numbers]

        # Location
        locations = soup.select('p.item-intro span.location')
        locations = [l.text for l in locations]

        # Tags
        tags = soup.select("li.ui-crumb.breadcrumb a span")
        tags = [t.text for t in tags]

        # Keys
        metas_ = soup.select('div.item-properties dl')
        metas = {}
        for m in metas_:
            key = m.select('dt')
            key = key[0].text if key and len(key) > 0 else ''
            value = m.select('dd')
            value = value[0].text if value and len(value) > 0 else ''

            metas[key] = value

        item = ClassifiedWebCrawlerItem()
        item["title"] = title
        item["description"] = content
        item["price"] = 0
        item["seller_name"] = person_name
        item["seller_number"] = contact_numbers
        item["location"] = locations
        item["tags"] = tags
        item["metas"] = metas
        item["raw"] = soup.text

        yield item
