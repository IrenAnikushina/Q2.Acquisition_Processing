# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    source_user = scrapy.Field()  # По юзеру разбила БД на коллекции
    user_id = scrapy.Field()
    username = scrapy.Field()
    full_name = scrapy.Field()
    profile_pic_url = scrapy.Field()
    follower_data = scrapy.Field()
    status = scrapy.Field()  # По статусу ясно кто это - юзер из подписок 'subscription' или подписчик 'follower'
