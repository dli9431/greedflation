# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from spider.items import ProductItem, PriceItem
import pymongo
from datetime import datetime

class GreedflationDBPipeline:
    collection_name_products = "products"
    collection_name_prices = "prices"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(spider.settings.get('MONGO_URI'))
        self.db = self.client[spider.settings.get('MONGO_DATABASE')]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, ProductItem):
            self.db[self.collection_name_products].insert_one(dict(item))
        elif isinstance(item, PriceItem):
            if 'date' in item:
                item['date'] = datetime.combine(item['date'], datetime.min.time())  # convert date to datetime
                self.db[self.collection_name_prices].insert_one(dict(item))
        return item