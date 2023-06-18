# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from spider.items import ProductItem, PriceItem
import pymongo
from datetime import datetime

# Your Pipeline code
class GreedflationDBPipeline:
    collection_name_products = "products"
    collection_name_prices = "prices"
    collection_name_scraped = "scraped"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(spider.settings.get('MONGO_URI'))
        self.db = self.client[spider.settings.get('MONGO_DATABASE')]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider, payload=None):
        if isinstance(item, ProductItem):
            self.db[self.collection_name_products].insert_one(dict(item))
        elif isinstance(item, PriceItem):
            self.db[self.collection_name_prices].insert_one(dict(item))
            if payload:  # ensure payload is not None
                self.mark_as_scraped(spider.url, payload)
        return item

    def has_been_scraped(self, url, pagination_from, pagination_size):
        scraped_pages = self.db[self.collection_name_scraped]
        return scraped_pages.count_documents({'url': url, 'pagination_from': pagination_from, 'pagination_size': pagination_size}) > 0

    def mark_as_scraped(self, url, payload):
        pagination_from = payload['pagination']['from']
        pagination_size = payload['pagination']['size']
        self.db[self.collection_name_scraped].insert_one({'url': url, 'pagination_from': pagination_from, 'pagination_size': pagination_size, 'timestamp': datetime.utcnow()})
