import scrapy
from scrapy.crawler import CrawlerProcess
from spider import DaftSpider


def lambda_handler(event, context):
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
    })

    process.crawl(DaftSpider)
    process.start()
