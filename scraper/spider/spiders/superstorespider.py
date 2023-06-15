import json
import scrapy
from scraper.spider.items import ProductItem, PriceItem

class SuperstoreSpider(scrapy.Spider):
    name = 'superstore_spider'
    url = 'https://api.pcexpress.ca/product-facade/v3/products/category/listing'

    def start_requests(self):
        payload = {
            "pagination": {"from": 0, "size": 50},
            "banner": "superstore",
            "cartId": "5d1f7722-6085-4f8e-b854-9bdd3e7d11ec",
            "lang": "en",
            "storeId": "1517",
            "pcId": None,
            "pickupType": "STORE",
            "offerType": "ALL",
            "categoryId": "27998"
        }
        yield scrapy.Request(self.url, method='POST', body=json.dumps(payload),
                             headers={'Content-Type': 'application/json'}, cb_kwargs=dict(payload=payload))

    def parse(self, response, payload):
        data = json.loads(response.body)
        for product in data['results']:
            product_item = ProductItem(
                name=product['name'],
                brand=product['brand'],
                link=product['link'],
            )
            yield product_item
            price_item = PriceItem(
                product_id=product_item['product_id'],
                price=product['prices']['price']['value'],
                comparison_price=product['prices']['comparisonPrices'][0]['value'] if product['prices']['comparisonPrices'] else None,
            )
            yield price_item

        # Pagination logic
        if data['results']:  # assuming that the presence of 'results' means there's more data
            payload['pagination']['from'] += payload['pagination']['size']
            yield scrapy.Request(self.url, method='POST', body=json.dumps(payload),
                                 headers={'Content-Type': 'application/json'}, cb_kwargs=dict(payload=payload))
