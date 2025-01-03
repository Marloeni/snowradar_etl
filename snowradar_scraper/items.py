# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class OnthesnowItem(scrapy.Item):
    name = scrapy.Field()
    snowfall_24h = scrapy.Field()
    base_depth = scrapy.Field()
    open_trails = scrapy.Field()
    total_trails = scrapy.Field()
    open_lifts = scrapy.Field()
    total_lifts = scrapy.Field()