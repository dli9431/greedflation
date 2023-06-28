import json
import scrapy
from datetime import datetime, timedelta
from spider.items import ProductItem, PriceItem
import pymongo
from . import payload as pyld


def get_db():
    client = pymongo.MongoClient('mongodb://db:27017/')
    return client['superstoredb']


class SuperstoreSpider(scrapy.Spider):
    name = 'superstore_spider'
    url = 'https://api.pcexpress.ca/product-facade/v3/products/category/listing'
    headers = pyld.headers

    def __init__(self, *args, **kwargs):
        super(SuperstoreSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient('mongodb://db:27017/')
        self.db = self.client['superstoredb']
        self.collection_name_scraped = "scraped"

    # set to 1 minute for testing purposes
    def has_been_scraped(self, url, payload, hours=.01667):
        pagination_from = payload['pagination']['from']
        pagination_size = payload['pagination']['size']

        # X hours before the current time
        x_hours_ago = datetime.utcnow() - timedelta(hours=hours)

        # Search for a document with the given URL and pagination inserted within the past X hours
        document = self.db[self.collection_name_scraped].find_one({
            'url': url,
            'pagination_from': pagination_from,
            'pagination_size': pagination_size,
            'timestamp': {'$gte': x_hours_ago}
        })

        # If a document is found, return True, indicating the page has already been scraped
        # within the past X hours. Otherwise, return False.
        if document is None:
            return False
        else:
            return True

    def mark_as_scraped(self, url, payload):
        pagination_from = payload['pagination']['from']
        pagination_size = payload['pagination']['size']
        self.db[self.collection_name_scraped].insert_one(
            {'url': url, 'pagination_from': pagination_from,
             'pagination_size': pagination_size, 'timestamp': datetime.utcnow()})

    def start_requests(self):
        payload = pyld.generate_payload(50, 0)

        if not self.has_been_scraped(self.url, payload):
            yield scrapy.Request(
                self.url,
                method='POST',
                body=json.dumps(payload),
                headers=self.headers,
                cb_kwargs=dict(payload=payload)
            )

    def parse(self, response, payload):
        print('parse')
        data = json.loads(response.body)
        for product in data['results']:
            product_item = ProductItem(
                product_code=product['code'],
                name=product['name'],
                brand=product['brand'],
                url=product['link'],
                size=product['packageSize']
            )

            # Check if the product already exists in the database
            existing_product = self.db.products.find_one(
                {"product_code": product_item["product_code"]})

            if not existing_product:
                # Insert a new product document
                self.db.products.insert_one(dict(product_item))

            price_item = PriceItem(
                product_code=product['code'],
                price=product['prices']['price']['value'],
                type=product['prices']['price']['type'],
                date=datetime.utcnow()
            )

            # Check if the price already exists in the database
            existing_product_price = self.db.prices.find_one(
                {"product_code": price_item["product_code"]})

            # If product doesn't exist in the price collection
            if not existing_product_price:
                # Insert a new price document
                self.db.prices.insert_one(dict(price_item))

            # If product does exist in the price collection
            else:
                # Find the most recent price entry for this product
                last_price = self.db.prices.find_one(
                    {"product_code": price_item["product_code"]}, sort=[("date", pymongo.DESCENDING)])

                # Check if the price has changed since the last scrape
                if last_price["price"] != price_item["price"]:
                    # If the price has changed, insert a new price document
                    self.db.prices.insert_one(dict(price_item))

                else:
                    # If the price has not changed, check if the existing date is older than 24 hours
                    time_difference = datetime.utcnow() - last_price["date"]
                    if time_difference.total_seconds() >= 24*60*60:  # if difference is more than 24 hours
                        # If existing date is older than 24 hours, insert a new record
                        self.db.prices.insert_one(dict(price_item))

        # Mark page as scraped
        self.mark_as_scraped(self.url, payload)

        # Pagination logic
        if data['results']:
            payload['pagination']['from'] += 1
            if not self.has_been_scraped(self.url, payload):
                yield scrapy.Request(self.url, method='POST', body=json.dumps(payload),
                                     headers=self.headers, cb_kwargs=dict(payload=payload))
