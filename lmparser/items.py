# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def transform(data):
    return ''.join(data.split())


# def s_to_b(link):
#     if link:
#         link = link.replace('w_82,h_82', 'w_2000,h_2000')
#     return link


class LmparserItem(scrapy.Item):
    _id = scrapy.Field()
    item_name = scrapy.Field(output_processor=TakeFirst())
    item_photo = scrapy.Field()
    item_link = scrapy.Field(output_processor=TakeFirst())
    item_price = scrapy.Field(input_processor=MapCompose(transform), output_processor=TakeFirst())
    spec_name = scrapy.Field()
    spec_value = scrapy.Field(input_processor=MapCompose(transform))
    specifications = scrapy.Field()
