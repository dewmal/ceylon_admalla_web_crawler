# -*- coding: utf-8 -*-
import datetime

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
        self.parse(response)
        self.driver.get(response.url)
        all_show_number = self.driver.find_element_by_css_selector("span.gtm-show-number")
        all_show_number.click()

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        title = soup.select("title")[0]
        title = title.text if title else ''

        metatags = soup.find_all('meta', attrs={'name': 'robots'})
        expire_date = ""
        for tag in metatags:
            val = f'{tag.attrs["content"].lower()}'
            if val.startswith("noarchive,nofollow,unavailable_after:"):
                expire_date = val.replace("noarchive,nofollow,unavailable_after:", "")
                break

        metatags = soup.find_all('meta', attrs={'property': 'og:image'})
        base_image = ""
        for tag in metatags:
            base_image = f'{tag.attrs["content"].lower()}'
            break

            # noarchive, nofollow, unavailable_after:

        post_date = soup.select(
            "html body.on-item-detail div.app-content div.container.main div.ui-panel.is-rounded.item-detail div.ui-panel-content.ui-panel-block div.row.lg-g div.item-top.col-12.lg-8 p.item-intro span.date")[
            0]
        post_date = post_date.text if post_date else ''

        # expire_date = soup.select(
        #     "head > meta:nth-child(33)")[
        #     0]
        # expire_date = post_date if post_date else ''

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
        # Location
        price = soup.select(
            'html body.on-item-detail div.app-content div.container.main div.ui-panel.is-rounded.item-detail div.ui-panel-content.ui-panel-block div.row.lg-g div.col-12.lg-8.item-body div.row.lg-g div.col-12.lg-8 div.item-price div.ui-price div.ui-price-tag span.amount')
        price = [l.text for l in locations]

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
        item["crawler_name"] = self.name
        item["url"] = response.url
        item["base_image"] = base_image
        item["title"] = title
        item["description"] = content
        item["price"] = price
        item["seller_name"] = person_name
        item["seller_number"] = contact_numbers
        item["location"] = locations
        item["tags"] = tags
        item["metas"] = metas
        item["raw_data"] = soup.text
        item["create_date"] = post_date
        item["expire_date"] = expire_date
        item["crawled_date"] = datetime.datetime.now()

        yield item
