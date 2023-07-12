import re
import json
import scrapy
from datetime import datetime, timedelta
from spider.items import ProductItem, PriceItem
import pymongo
from . import payload as pyld


def get_db():
    client = pymongo.MongoClient('mongodb://db:27017/')
    return client['superstoredb']

def total_macros(price, size, size_unit, serving_size, serving_size_unit, protein, protein_unit, carb, carb_unit, 
                 fat, fat_unit, fiber, fiber_unit, calories):
    # Check if all units are the same
    if serving_size_unit != fat_unit or serving_size_unit != fiber_unit or serving_size_unit != protein_unit or serving_size_unit != carb_unit:
        return None

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

    # Calculate serving size multiplier if size unit is different from serving size unit
    multiplier = 1
    if size_unit != serving_size_unit:
        if serving_size_unit in conversion_factors and size_unit in conversion_factors[serving_size_unit]:
            multiplier = conversion_factors[serving_size_unit][size_unit]
        else:
            return None

    # Calculate number of servings in the product
    num_servings = size * multiplier / serving_size if serving_size != 0 else 0
    
    # Calculate total macros
    total_fat = fat * num_servings
    total_protein = protein * num_servings
    total_carb = carb * num_servings
    total_fiber = fiber * num_servings
    total_calories = calories * num_servings

    # Calculate price per macro
    price_per_fat = price / total_fat if total_fat != 0 else 0
    price_per_protein = price / total_protein if total_protein != 0 else 0
    price_per_carb = price / total_carb if total_carb != 0 else 0
    price_per_fiber = price / total_fiber if total_fiber != 0 else 0

    # calculate price per serving
    price_per_serving = price / num_servings if num_servings != 0 else 0

    return {'total_fat': total_fat, 'total_protein': total_protein, 'total_carb': total_carb, 'total_fiber': total_fiber, 
            'total_servings': num_servings, 'price_per_fat': price_per_fat, 'price_per_protein': price_per_protein,
            'price_per_carb': price_per_carb, 'price_per_fiber': price_per_fiber, 'price_per_serving': price_per_serving,
            'total_calories': total_calories}

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
        query = {'product_code': '21098010_KG'}
        document = self.products.find_one(query)
        if (document):
            projection = {'_id': 0, 'price': 1, 'size': 1, 'size_unit': 1, 'type': 1, 'date': 1}
            sort = [('date', pymongo.DESCENDING)]
            price_item = self.prices.find_one(query, projection=projection, sort=sort)

            if price_item:
                document['price'] = price_item['price']
                document['size'] = price_item['size']
                document['size_unit'] = price_item['size_unit']

            req = self.url + \
                pyld.generate_product_payload(document['product_code'])           
            yield scrapy.Request(
                req,
                method='GET',
                headers=self.headers,
                cb_kwargs=dict(item=document)
            )
        # # Find documents without the 'scraped_nutrition' field
        # query = {'scraped_nutrition': {'$exists': False}}
        # documents = self.products.find(query)
    
        # # Extract the URLs and create start URLs for scraping
        # for document in documents:
        #     if document:
        #         query = {'product_code': document['product_code']}
        #         projection = {'_id': 0, 'price': 1, 'size': 1, 'size_unit': 1, 'type': 1, 'date': 1}
        #         sort = [('date', pymongo.DESCENDING)]
        #         price_item = self.prices.find_one(query, projection=projection, sort=sort)

        #         # Assign the price fields to the ProductItem
        #         if price_item:
        #             document['price'] = price_item['price']
        #             document['size'] = price_item['size']
        #             document['size_unit'] = price_item['size_unit']

        #         req = self.url + \
        #             pyld.generate_product_payload(document['product_code'])           
        #         yield scrapy.Request(
        #             req,
        #             method='GET',
        #             headers=self.headers,
        #             cb_kwargs=dict(item=document)
        #         )

    def parse(self, response, item):
        if (response.status != 404):
            item['scraped_nutrition'] = False

        data = json.loads(response.body)
        
        # Extract ingredients
        item['ingredients'] = data.get('ingredients')
        
        # Extract the nutrition facts section
        nutrition_facts = data.get('nutritionFacts', [])

        if nutrition_facts:
            # Extract the first item from the nutrition facts list
            nutrition_info = nutrition_facts[0]

            # Extract specific fields from the nutrition info and assign them to the item
            calories_match = None
            if nutrition_info.get('calories'):
                calories_match = re.match(r'^([\d\.]+)\s*(\w+)$', nutrition_info['calories']['valueInGram'])
            if calories_match:
                item['calories'] = float(calories_match.group(1))
                item['calories_unit'] = calories_match.group(2)

            fat_match = None
            if nutrition_info.get('totalFat'):
                fat_match = re.match(r'^([\d\.]+)\s*(\w+)$', nutrition_info['totalFat']['valueInGram'])
            if fat_match:
                item['fat'] = float(fat_match.group(1))
                item['fat_unit'] = fat_match.group(2)

            fiber_match = None
            carb_match = None
            if nutrition_info.get('totalCarbohydrate'):
                carb_match = re.match(r'^([\d\.]+)\s*(\w+)$', nutrition_info['totalCarbohydrate']['valueInGram'])
                for nutrient in nutrition_info['totalCarbohydrate'].get('subNutrients', []):
                    if nutrient.get('code') == 'dietaryFiber':
                        fiber_match = re.match(r'^([\d\.]+)\s*(\w+)$', nutrient['valueInGram'])

            if carb_match:
                item['carb'] = float(carb_match.group(1))
                item['carb_unit'] = carb_match.group(2)

            if fiber_match:
                item['fiber'] = float(fiber_match.group(1))
                item['fiber_unit'] = fiber_match.group(2)

            protein_match = None
            if nutrition_info.get('protein'):
                protein_match = re.match(r'^([\d\.]+)\s*(\w+)$', nutrition_info['protein']['valueInGram'])
            if protein_match:
                item['protein'] = float(protein_match.group(1))
                item['protein_unit'] = protein_match.group(2)

            serving_size_match = None
            if nutrition_info.get('topNutrition') and nutrition_info['topNutrition'][0].get('valueInGram'):
                serving_size_match = re.match(r'^([\d\.]+)\s*(\w+)$', nutrition_info['topNutrition'][0]['valueInGram'])
            if serving_size_match:
                item['serving_size'] = float(serving_size_match.group(1))
                item['serving_size_unit'] = serving_size_match.group(2)

            if 'price' in item and 'size' in item and 'size_unit' in item and 'serving_size' in item and 'serving_size_unit' in item and 'protein' in item and 'protein_unit' in item and 'carb' in item and 'carb_unit' in item and 'fat' in item and 'fat_unit' in item and 'fiber' in item and 'fiber_unit' in item:
                total = total_macros(item['price'], item['size'], item['size_unit'], item['serving_size'], item['serving_size_unit'], 
                                            item['protein'], item['protein_unit'], item['carb'], item['carb_unit'],
                                            item['fat'], item['fat_unit'], item['fiber'], item['fiber_unit'], item['calories'])
                
                if total is not None and all(key in total for key in ['total_fat', 'total_protein', 'total_carb', 'total_fiber', 'total_servings', 
                                                     'price_per_fat', 'price_per_protein', 'price_per_carb', 'price_per_fiber', 
                                                     'price_per_serving']):
                    item['price_per_serving'] = total['price_per_serving']
                    item['price_per_protein'] = total['price_per_protein']
                    item['price_per_carb'] = total['price_per_carb']
                    item['price_per_fat'] = total['price_per_fat']
                    item['price_per_fiber'] = total['price_per_fiber']
                    item['total_protein'] = total['total_protein']
                    item['total_carb'] = total['total_carb']
                    item['total_fat'] = total['total_fat']
                    item['total_fiber'] = total['total_fiber']
                    item['total_calories'] = total['total_calories']
                    item['total_servings'] = total['total_servings']
                    
                # If we've done all the calculations on nutrition data set scraped_nutrition to True
                item['scraped_nutrition'] = True

        # If item has no nutrition data, set scraped_nutrition to False
        item['scraped_nutrition'] = False

        # Update the document in the database
        query = {'_id': item['_id']}
        update = {'$set': item }
        self.products.update_one(query, update)

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

    def mark_as_scraped(self, url, payload):
        pagination_from = payload['pagination']['from']
        pagination_size = payload['pagination']['size']
        self.db[self.collection_name_scraped].insert_one(
            {'url': url, 'pagination_from': pagination_from,
             'pagination_size': pagination_size, 'timestamp': datetime.utcnow()})

    def start_requests(self):
        print('start_requests')
        payload = pyld.generate_payload(50, 0)
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
                product_code=product['code'],
                name=product['name'],
                brand=product['brand'],
                url=product['link'],
                # size=product['packageSize']
            )

            # Check if the product already exists in the database
            existing_product = self.db.products.find_one(
                {"product_code": product_item["product_code"]})

            if not existing_product:
                # Insert a new product document
                self.db.products.insert_one(dict(product_item))
        
            # Check if the package size is available
            match_size = re.match(r'^([\d\.]+)\s*(\w+)$', product.get('packageSize'))
            if match_size:
                size = float(match_size.group(1))
                size_unit = match_size.group(2)
            else:
                size = None
                size_unit = None

            # Check for average weight/uom if it exists
            average_weight = product['averageWeight'] if 'averageWeight' in product else None
            uom = product['uom'] if average_weight is not None else None

            price_item = PriceItem(
                product_code=product['code'],
                price=product['prices']['price']['value'],
                type=product['prices']['price']['type'],
                date=datetime.utcnow(),
                size=average_weight if size is None else size,
                size_unit=uom if size_unit is None else size_unit
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

                # Check if the price or size has changed since the last scrape
                if last_price["price"] != price_item["price"] or last_price.get("size") != price_item.get("size"):
                    # If the price or package size has changed, insert a new price document
                    self.db.prices.insert_one(dict(price_item))

        # Mark page as scraped
        self.mark_as_scraped(self.url, payload)

        # Pagination logic
        if data['results']:
            payload['pagination']['from'] += 1
            if not self.has_been_scraped(self.url, payload):
                yield scrapy.Request(self.url, method='POST', body=json.dumps(payload),
                                     headers=self.headers, cb_kwargs=dict(payload=payload))
