import json
import scrapy
from datetime import datetime
from spider.items import ProductItem, PriceItem
from pymongo import MongoClient


class SuperstoreInitSpider(scrapy.Spider):
    name = 'init_superstore_spider'
    url = 'https://www.realcanadiansuperstore.ca/food/meat/c/27998?navid=flyout-L2-Meat'

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        print(response.body)


def get_db():
    client = MongoClient('mongodb://db:27017/')
    return client['superstoredb']


class SuperstoreSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super(SuperstoreSpider, self).__init__(*args, **kwargs)
        self.client = MongoClient('mongodb://db:27017/')
        self.db = self.client['superstoredb']
        self.collection_name_scraped = "scraped"

    def has_been_scraped(self, url, payload):
        pagination_from = payload['pagination']['from']
        pagination_size = payload['pagination']['size']
        return self.db[self.collection_name_scraped].count_documents(
            {'url': url, 'pagination_from': pagination_from, 'pagination_size': pagination_size}) > 0

    def mark_as_scraped(self, url, payload):
        pagination_from = payload['pagination']['from']
        pagination_size = payload['pagination']['size']
        self.db[self.collection_name_scraped].insert_one(
            {'url': url, 'pagination_from': pagination_from,
             'pagination_size': pagination_size, 'timestamp': datetime.utcnow()})

    name = 'superstore_spider'
    url = 'https://api.pcexpress.ca/product-facade/v3/products/category/listing'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en",
        "Business-User-Agent": "PCX-Web",
        "Content-Type": "application/json",
        "Host": "api.pcexpress.ca",
        "Origin": "https://www.realcanadiansuperstore.ca",
        "Referer": "https://www.realcanadiansuperstore.ca",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        "Site-Banner": "superstore",
        "x-apikey": "1im1hL52q9xvta16GlSdYDsTsG0dmyhF",
    }

    def start_requests(self):
        page_from = 0
        page_size = 50
        payload = {
            "pagination": {"from": page_from, "size": page_size},
            "banner": "superstore",
            # generate this based on initial request later
            "cartId": "5d1f7722-6085-4f8e-b854-9bdd3e7d11ec",
            "lang": "en",
            "storeId": "1517",
            "pcId": None,
            "pickupType": "STORE",
            "offerType": "ALL",
            "categoryId": "27998",
        }
        if not self.has_been_scraped(self.url, payload):
            yield scrapy.Request(self.url, method='POST', body=json.dumps(payload),
                                 headers=self.headers, cb_kwargs=dict(payload=payload))

    def parse(self, response, payload):
        data = json.loads(response.body)
        for product in data['results']:
            product_item = ProductItem(
                product_id=product['code'],
                name=product['name'],
                brand=product['brand'],
                # product_description=product['description'],
                url=product['link'],
                size=product['packageSize']
            )
            yield product_item
            price_item = PriceItem(
                product_id=product['code'],
                price=product['prices']['price']['value'],
                type=product['prices']['price']['type'],
                date=datetime.utcnow()
            )
            yield price_item

        # Mark page as scraped
        self.mark_as_scraped(self.url, payload)

        # Pagination logic
        if data['results']:
            payload['pagination']['from'] += 1
            if not self.has_been_scraped(self.url, payload):
                yield scrapy.Request(self.url, method='POST', body=json.dumps(payload),
                                     headers=self.headers, cb_kwargs=dict(payload=payload))
