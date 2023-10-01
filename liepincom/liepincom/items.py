# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class LiepincomItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    position = scrapy.Field()
    city = scrapy.Field()
    salary = scrapy.Field()
    year = scrapy.Field()
    edu = scrapy.Field()
    company = scrapy.Field()
    company_size = scrapy.Field()
