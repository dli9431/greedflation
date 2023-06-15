# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProductItem(scrapy.Item):
    product_id = scrapy.Field()
    name = scrapy.Field()
    product_description = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    size = scrapy.Field() # grams
    calories = scrapy.Field() # kcal
    protein = scrapy.Field() # grams
    carbs = scrapy.Field() # grams
    fat = scrapy.Field() # grams

class PriceItem(scrapy.Item):
    product_id = scrapy.Field()
    price = scrapy.Field()
    type = scrapy.Field() # regular, special, etc.
    date = scrapy.Field()