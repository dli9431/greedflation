# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scraper.spider.items import ProductItem, PriceItem
import pymongo

class GreedflationDBPipeline:
    collection_name_products = "products"
    collection_name_prices = "prices"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(spider.settings.get('MONGO_URI'))
        self.db = self.client[spider.settings.get('MONGO_DATABASE')]

    def close_spider(self, spider):
        self.client.close()
