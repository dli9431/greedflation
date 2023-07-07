# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProductItem(scrapy.Item):
    product_code = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    product_description = scrapy.Field()
    url = scrapy.Field()
    size = scrapy.Field() # float
    size_unit = scrapy.Field() # grams, kg, ml, etc.
    serving_size = scrapy.Field() # serving size, grams for now
    calories = scrapy.Field() # kcal
    protein = scrapy.Field() # grams
    carbs = scrapy.Field() # grams
    fat = scrapy.Field() # grams
    ingredients = scrapy.Field() # ingredients

class PriceItem(scrapy.Item):
    product_code = scrapy.Field()
    price = scrapy.Field()
    type = scrapy.Field() # regular, special, etc.
    date = scrapy.Field()