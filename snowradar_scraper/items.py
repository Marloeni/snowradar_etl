# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SkiresortItem(scrapy.Item):
    name = scrapy.Field()
    slopes = scrapy.Field()
    lifts = scrapy.Field()
    snow = scrapy.Field()
    weather = scrapy.Field()
