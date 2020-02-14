from shutil import which

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from classified_web_crawler.classified_web_crawler import settings
from classified_web_crawler.classified_web_crawler.spiders.ikman import IkmanSpider

# from classified_web_crawler.classified_web_crawler.middlewares import SeleniumMiddleware
import chromedriver_binary

process = CrawlerProcess(settings={
    "SELENIUM_DRIVER_NAME": 'chrome',
    "SELENIUM_DRIVER_EXECUTABLE_PATH": which('chromedriver'),
    "SELENIUM_DRIVER_ARGUMENTS": ['-headless', '--disable-gpu', '--log-level=3']
    # '--headless' if using chrome instead of firefox
    ,
    "DOWNLOADER_MIDDLEWARES": {
        'scrapy_selenium.SeleniumMiddleware': 800
    }
})

process.crawl(IkmanSpider)
process.start()  # the script will block here until the crawling is finished
