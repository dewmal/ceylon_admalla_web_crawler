from scrapy.crawler import CrawlerProcess

from classified_web_crawler.classified_web_crawler.spiders.ikman import IkmanSpider

# from classified_web_crawler.classified_web_crawler.middlewares import SeleniumMiddleware

process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
})

process.crawl(IkmanSpider)
process.start()  # the script will block here until the crawling is finished
