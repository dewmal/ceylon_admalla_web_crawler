import time
import pycron


def process_crawler():
    from shutil import which

    from scrapy.crawler import CrawlerProcess

    from classified_web_crawler.spiders.hitad import HitadSpider
    from classified_web_crawler.spiders.ikman import IkmanSpider

    # from classified_web_crawler.classified_web_crawler.middlewares import SeleniumMiddleware
    # import chromedriver_binary

    process = CrawlerProcess(settings={
        "SELENIUM_DRIVER_NAME": 'chrome',
        "SELENIUM_DRIVER_EXECUTABLE_PATH": which('chromedriver'),
        "SELENIUM_DRIVER_ARGUMENTS": ['-headless', '--disable-gpu', '--log-level=3']
        # '--headless' if using chrome instead of firefox
        ,
        "MONGO_URI": "mongodb://root:br2n4P3gqotR@44.233.75.14:27017",
        "MONGO_DATABASE": "classified_crawler",
        "ITEM_PIPELINES": {
            'classified_web_crawler.pipelines.ClassifiedWebCrawlerPipeline': 300,
        },
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 0.25,
        "AUTOTHROTTLE_MAX_DELAY": 4,
        "DEPTH_PRIORITY": 1,
        "SCHEDULER_DISK_QUEUE": 'scrapy.squeues.PickleFifoDiskQueue',
    })

    process.crawl(IkmanSpider)
    process.crawl(HitadSpider)
    process.start()


process_crawler()
# while True:
#     if pycron.is_now('0 */4 * * *'):  # True Every Sunday at 02:00
#
#     time.sleep(60)
