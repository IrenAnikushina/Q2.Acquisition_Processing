# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import scrapy
from pymongo import MongoClient
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class LmparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.lmDB = client.LM_scrapy

    def process_item(self, item, spider):
        item['specifications'] = dict(zip(item['spec_name'], item['spec_value']))
        collection = self.lmDB[spider.name]
        collection.insert_one({
            'item_name': item['item_name'],
            'item_photo': item['item_photo'],
            'item_link': item['item_link'],
            'item_price': item['item_price'],
            'specifications': item['specifications']
        })
        return item


class LMPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['item_photo']:
            for img in item['item_photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        dir = item['item_name']
        image_guide = request.url.split('/')[-1]
        return f'{dir}/img{image_guide}'

    def item_completed(self, results, item, info):
        if results:
            item['item_photo'] = [itm[1] for itm in results if itm[0]]
        return item
