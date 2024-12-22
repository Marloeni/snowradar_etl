# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SkiresortItem(scrapy.Item):
    name = scrapy.Field()
    opened_slopes = scrapy.Field()
    total_slopes = scrapy.Field()
    opened_lifts = scrapy.Field()
    total_lifts = scrapy.Field()
    snow = scrapy.Field()
    status = scrapy.Field()
    low_temp = scrapy.Field()
    high_temp = scrapy.Field()
    location = scrapy.Field()