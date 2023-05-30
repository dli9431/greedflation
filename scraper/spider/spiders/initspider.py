import scrapy

class InitSpider(scrapy.Spider):
    name = 'initspider'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    def parse(self, response):
        pass