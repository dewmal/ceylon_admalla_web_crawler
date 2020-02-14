from shutil import which

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from classified_web_crawler.classified_web_crawler import settings
from classified_web_crawler.classified_web_crawler.spiders.hitad import HitadSpider
from classified_web_crawler.classified_web_crawler.spiders.ikman import IkmanSpider

# from classified_web_crawler.classified_web_crawler.middlewares import SeleniumMiddleware
import chromedriver_binary

process = CrawlerProcess(settings={
    "SELENIUM_DRIVER_NAME": 'chrome',
    "SELENIUM_DRIVER_EXECUTABLE_PATH": which('chromedriver'),
    "SELENIUM_DRIVER_ARGUMENTS": ['-headless', '--disable-gpu', '--log-level=3']
    # '--headless' if using chrome instead of firefox
    ,
    "MONGO_URI": "mongodb://root:br2n4P3gqotR@44.233.75.14:27017",
    "MONGO_DATABASE": "classified_crawler",
    "ITEM_PIPELINES": {
        'classified_web_crawler.classified_web_crawler.pipelines.ClassifiedWebCrawlerPipeline': 300,
    },
    "AUTOTHROTTLE_ENABLED": True,
    "AUTOTHROTTLE_START_DELAY": 0.25,
    "AUTOTHROTTLE_MAX_DELAY": 4
})

process.crawl(IkmanSpider)
process.crawl(HitadSpider)
process.start()  # the script will block here until the crawling is finished
