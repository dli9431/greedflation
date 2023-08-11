import re
import json
import scrapy
from datetime import datetime, timedelta
from spider.items import ProductItem, PriceItem, StoreItem
import pymongo
from . import payload as pyld


def get_db():
    client = pymongo.MongoClient('mongodb://db:27017/')
    return client['superstoredb']


def calc_multiplier(size_unit, serving_size_unit):
    # Define conversion factors
    conversion_factors = {
        'g': {
            'kg': 0.001,
            'oz': 0.035274,
            'lb': 0.00220462
        },
        'kg': {
            'g': 1000,
            'oz': 35.274,
            'lb': 2.20462
        },
        'oz': {
            'g': 28.3495,
            'kg': 0.0283495,
            'lb': 0.0625
        },
        'lb': {
            'g': 453.592,
            'kg': 0.453592,
            'oz': 16
        },
        'ml': {
            'l': 0.001,
            'fl oz': 0.033814,
            'cup': 0.00422675
        },
        'l': {
            'ml': 1000,
            'fl oz': 33.814,
            'cup': 4.22675
        },
        'fl oz': {
            'ml': 29.5735,
            'l': 0.0295735,
            'cup': 0.123223
        },
        'cup': {
            'ml': 236.588,
            'l': 0.236588,
            'fl oz': 8.11537
        }
    }
    if size_unit.lower() != serving_size_unit.lower():
        if size_unit.lower() in conversion_factors and serving_size_unit.lower() in conversion_factors[size_unit.lower()]:
            if conversion_factors[size_unit.lower()][serving_size_unit.lower()] > 1:
                return conversion_factors[size_unit.lower()][serving_size_unit.lower()]
            else:
                return 1 / conversion_factors[serving_size_unit.lower()][size_unit.lower()]
        else:
            return None


class SuperstoreProductsSpider(scrapy.Spider):
    name = 'superstore_products_spider'
    url = 'https://api.pcexpress.ca/product-facade/v4/products'
    headers = pyld.v4_headers

    def __init__(self, *args, **kwargs):
        super(SuperstoreProductsSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient('mongodb://db:27017/')
        self.db = self.client['superstoredb']
        self.products = self.db['products']
        self.prices = self.db['prices']

    def start_requests(self):
        # # testing code (1 item)
        # query = {'product_code': '20804532_KG'}
        # document = self.products.find_one(query)
        # if (document):
        #     projection = {'_id': 0, 'price': 1, 'size': 1, 'size_unit': 1, 'type': 1, 'date': 1}
        #     sort = [('date', pymongo.DESCENDING)]
        #     price_item = self.prices.find_one(query, projection=projection, sort=sort)

        #     if price_item:
        #         req = self.url + \
        #             pyld.generate_product_payload(document['product_code'])
        #         yield scrapy.Request(
        #             req,
        #             method='GET',
        #             headers=self.headers,
        #             cb_kwargs=dict(item=document, price_item=price_item)
        #         )

        # Find documents without the 'scraped_nutrition' field
        query = {'scraped_nutrition': {'$exists': False}}
        documents = self.products.find(query)

        # Extract the URLs and create start URLs for scraping
        for document in documents:
            if document:
                query = {'product_code': document['product_code']}
                projection = {'_id': 0, 'price': 1, 'size': 1,
                              'size_unit': 1, 'type': 1, 'date': 1}
                sort = [('date', pymongo.DESCENDING)]
                price_item = self.prices.find_one(
                    query, projection=projection, sort=sort)

                if price_item:
                    req = self.url + \
                        pyld.generate_product_payload(document['product_code'])
                    yield scrapy.Request(
                        req,
                        method='GET',
                        headers=self.headers,
                        cb_kwargs=dict(item=document, price_item=price_item)
                    )

    def clean_data(self, data, item, price_item):
        # Extract the nutrition facts section
        nutrition_facts = data.get('nutritionFacts', [])

        if nutrition_facts:
            # Extract the first item from the nutrition facts list
            nutrition_info = nutrition_facts[0]

            # Extract specific fields from the nutrition info and assign them to the item
            calories_match = None
            if nutrition_info.get('calories') is not None and nutrition_info['calories']['valueInGram'] is not None:
                calories_match = re.match(
                    r'^([\d\.]+)\s*(\w+)$', nutrition_info['calories']['valueInGram'])
            if calories_match:
                item['calories'] = float(calories_match.group(1))
                item['calories_unit'] = calories_match.group(2).lower()

            fat_match = None
            if nutrition_info.get('totalFat') is not None and nutrition_info['totalFat']['valueInGram'] is not None:
                fat_match = re.match(
                    r'^([\d\.]+)\s*(\w+)$', nutrition_info['totalFat']['valueInGram'])
            if fat_match:
                item['fat'] = float(fat_match.group(1))
                item['fat_unit'] = fat_match.group(2).lower()

            fiber_match = None
            carb_match = None
            if nutrition_info.get('totalCarbohydrate') is not None and nutrition_info['totalCarbohydrate']['valueInGram'] is not None:
                carb_match = re.match(
                    r'^([\d\.]+)\s*(\w+)$', nutrition_info['totalCarbohydrate']['valueInGram'])
                for nutrient in nutrition_info['totalCarbohydrate'].get('subNutrients', []):
                    if nutrient.get('code') == 'dietaryFiber':
                        fiber_match = re.match(
                            r'^([\d\.]+)\s*(\w+)$', nutrient['valueInGram'])

            if carb_match:
                item['carb'] = float(carb_match.group(1))
                item['carb_unit'] = carb_match.group(2).lower()

            if fiber_match:
                item['fiber'] = float(fiber_match.group(1))
                item['fiber_unit'] = fiber_match.group(2).lower()

            protein_match = None
            if nutrition_info.get('protein') is not None and nutrition_info['protein']['valueInGram'] is not None:
                protein_match = re.match(
                    r'^([\d\.]+)\s*(\w+)$', nutrition_info['protein']['valueInGram'])
            if protein_match:
                item['protein'] = float(protein_match.group(1))
                item['protein_unit'] = protein_match.group(2).lower()

            serving_size_match = None
            if nutrition_info.get('topNutrition') is not None and nutrition_info['topNutrition'][0].get('valueInGram') is not None:
                serving_size_match = re.match(
                    r'^([\d\.]+)\s*(\w+)$', nutrition_info['topNutrition'][0]['valueInGram'])
            if serving_size_match:
                item['serving_size'] = float(serving_size_match.group(1))
                item['serving_size_unit'] = serving_size_match.group(2).lower()

            # Calculate serving size multiplier if size unit is different from serving size unit
            multiplier = 1
            size = 0.0
            size_unit = ''

            # Check for pricing units type
            if ('uom' in price_item and price_item['uom'] is not None):
                size = float(price_item['average_weight'])
                size_unit = price_item['uom']
            elif ('size' in price_item and price_item['size'] is not None):
                size = float(price_item['size'])
                size_unit = price_item['size_unit']

            multiplier = calc_multiplier(size_unit, item['serving_size_unit'])

            if multiplier is not None:
                # Calculate number of servings in the product
                num_servings = size * multiplier / \
                    item['serving_size'] if item['serving_size'] != 0 else 0

                # Calculate total macros
                item['total_fat'] = item['fat'] * num_servings
                item['total_protein'] = item['protein'] * num_servings
                item['total_carb'] = item['carb'] * num_servings
                item['total_fiber'] = item['fiber'] * num_servings
                item['total_calories'] = item['calories'] * num_servings

                # Calculate price per macro
                item['price_per_fat'] = price_item['price'] / \
                    item['total_fat'] if item['total_fat'] != 0 else 0
                item['price_per_protein'] = price_item['price'] / \
                    item['total_protein'] if item['total_protein'] != 0 else 0
                item['price_per_carb'] = price_item['price'] / \
                    item['total_carb'] if item['total_carb'] != 0 else 0
                item['price_per_fiber'] = price_item['price'] / \
                    item['total_fiber'] if item['total_fiber'] != 0 else 0
                item['price_per_calories'] = price_item['price'] / \
                    item['total_calories'] if item['total_calories'] != 0 else 0

                # calculate price per serving
                item['price_per_serving'] = price_item['price'] / \
                    num_servings if num_servings != 0 else 0

        # Extract ingredients
        item['ingredients'] = data.get('ingredients')
        item['scraped_nutrition'] = True
        return item

    def parse(self, response, item, price_item):
        if (response.status != 404):
            item['scraped_nutrition'] = False

        data = json.loads(response.body)

        cleaned_item = self.clean_data(data, item, price_item)

        # Update the document in the database
        query = {'_id': cleaned_item['_id']}
        update = {'$set': cleaned_item}
        self.products.update_one(query, update)


class SuperstoreSpider(scrapy.Spider):
    name = 'superstore_spider'
    url = 'https://api.pcexpress.ca/product-facade/v3/products/category/listing'
    headers = pyld.headers
    page_from = 0
    page_size = 50
    store_id = 1517
    # category_id = 27998
    # meat, frozen, fruit/veg, dairy/eggs, pantry, international, fish/seafood, snacks, drinks, organic, deli, bakery, prepared
    category_ids = [27998, 28005, 28000, 28003, 28006, 58044,
                    27999, 57025, 28004, 28189, 28001, 28002, 27996]

    def __init__(self, *args, **kwargs):
        super(SuperstoreSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient('mongodb://db:27017/')
        self.db = self.client['superstoredb']
        self.collection_name_scraped = "scraped"

    # set to 1 minute for testing purposes
    def has_been_scraped(self, url, payload, hours=.01667):
        print('has_been_scraped')
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
            print('has_been_scraped: False')
            return False
        else:
            print('has_been_scraped: True')
            return True

    def generate_payload(self, cat_id):
        return {
            "pagination": {
                "from": self.page_from,
                "size": self.page_size
            },
            "banner": "superstore",
            # generate this based on initial request later
            "cartId": "5d1f7722-6085-4f8e-b854-9bdd3e7d11ec",
            "lang": "en",
            "storeId": self.store_id,
            "pcId": None,
            "pickupType": "STORE",
            "offerType": "ALL",
            "categoryId": cat_id,
        }

    def mark_as_scraped(self, url, payload):
        pagination_from = payload['pagination']['from']
        pagination_size = payload['pagination']['size']
        self.db[self.collection_name_scraped].insert_one(
            {'category_id': payload['categoryId'], 'store_id': payload['storeId'], 'url': url, 'pagination_from': pagination_from,
             'pagination_size': pagination_size, 'timestamp': datetime.utcnow()})

    def start_requests(self):
        print('start_requests')
        for cat_id in self.category_ids:
            payload = self.generate_payload(cat_id)
            print(payload)
            if not self.has_been_scraped(self.url, payload):
                yield scrapy.Request(
                    self.url,
                    method='POST',
                    body=json.dumps(payload),
                    headers=self.headers,
                    cb_kwargs=dict(payload=payload)
                )

    def parse(self, response, payload):
        print(response)
        data = json.loads(response.body)
        for product in data['results']:
            product_item = ProductItem(
                product_category=payload['categoryId'],
                product_code=product['code'],
                name=product['name'],
                brand=product['brand'],
                url=product['link'],
                # size=product['packageSize']
            )

            store_item = StoreItem(
                product_code=product['code'],
                store_id=payload['storeId'],
                store_name=payload['banner']
            )

            # Check if the product already exists in the database
            existing_product = self.db.products.find_one(
                {"product_code": product_item["product_code"]})

            if not existing_product:
                # Insert a new product document
                self.db.products.insert_one(dict(product_item))
            else:
                # Update the existing product document
                self.db.products.update_one(
                    {"product_code": product_item["product_code"]},
                    {"$set": dict(product_item)}
                )

            # Create initial price item
            price_item = PriceItem(
                product_code=product['code'],
                price=product['prices']['price']['value'],
                type=product['prices']['price']['type'],
                date=datetime.utcnow(),
            )

            # Check if the package size is available
            if product['pricingUnits']['type'].lower() == 'sold_by_each_priced_by_weight':
                price_item['comparison_price'] = product['prices']['comparisonPrices'][0]['value']
                price_item['comparison_unit'] = product['prices']['comparisonPrices'][0]['unit'].lower(
                )
                price_item['average_weight'] = product['averageWeight']
                price_item['uom'] = product['uom'].lower()
                price_item['pricing_units'] = product['pricingUnits']['type'].lower()

            if product['pricingUnits']['type'].lower() == 'sold_by_each':
                match_size = re.match(
                    r'^([\d\.]+)\s*(\w+)$', product['packageSize'])
                if match_size:
                    price_item['size'] = float(match_size.group(1))
                    price_item['size_unit'] = match_size.group(2).lower()
                    price_item['pricing_units'] = product['pricingUnits']['type'].lower()

            # Check if the product has an associated store
            existing_store_product = self.db.store_product.find_one(
                {"product_code": store_item["product_code"]})

            # If product doesn't exist in the store_product collection
            if not existing_store_product:
                # Insert a new price document
                self.db.store_product.insert_one(dict(store_item))

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

                # Check if the price or size has changed since the last scrape
                if last_price["price"] != price_item["price"] or last_price.get("size") != price_item.get("size"):
                    # If the price or package size has changed, insert a new price document
                    self.db.prices.insert_one(dict(price_item))
                # Check if the average weight has changed since the last scrape
                elif "average_weight" in last_price and "average_weight" in price_item and last_price["average_weight"] != price_item["average_weight"]:
                    # If the average weight has changed, insert a new price document
                    self.db.prices.insert_one(dict(price_item))

        # Mark page as scraped
        self.mark_as_scraped(self.url, payload)

        # Pagination logic
        if data['results']:
            payload['pagination']['from'] += 1
            if not self.has_been_scraped(self.url, payload):
                yield scrapy.Request(self.url, method='POST', body=json.dumps(payload),
                                     headers=self.headers, cb_kwargs=dict(payload=payload))
