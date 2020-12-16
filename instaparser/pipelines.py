# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.instaDB = client.insta_scrapy

    def process_item(self, item, spider):
        collection_name = item['source_user']
        collection = self.instaDB[collection_name]
        collection.insert_one({
            'source_user': item['source_user'],
            'user_id': item['user_id'],
            'username': item['username'],
            'full_name': item['full_name'],
            'profile_pic_url': item['profile_pic_url'],
            'follower_data': item['follower_data'],
            'status': item['status']
        })
        return item

