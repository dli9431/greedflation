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
    # size = scrapy.Field() # float
    # size_unit = scrapy.Field() # g, kg, ml, etc
    serving_size = scrapy.Field() # float
    serving_size_unit = scrapy.Field()
    calories = scrapy.Field() # float
    calories_unit = scrapy.Field()
    protein = scrapy.Field() # float
    protein_unit = scrapy.Field()
    carbs = scrapy.Field() # float
    carbs_unit = scrapy.Field()
    fat = scrapy.Field() # float
    fat_unit = scrapy.Field()
    fiber = scrapy.Field() # float
    fiber_unit = scrapy.Field()
    ingredients = scrapy.Field() # ingredients

class PriceItem(scrapy.Item):
    product_code = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    size_unit = scrapy.Field()
    type = scrapy.Field() # regular, special, etc.
    date = scrapy.Field()
    comparison_price = scrapy.Field()
    comparison_unit = scrapy.Field()
    average_weight = scrapy.Field()
    uom = scrapy.Field()