# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies_scrapy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        if spider.name == 'hhru':
            item['item_salary'] = self.salary_hh(item['item_salary'])
            # vacancy_name = item['item_name']
        elif spider.name == 'superjobru':
            item['item_salary'] = self.salary_sjru(item['item_salary'])
        vacancy_name = ''.join(item['item_name'])
        vacancy_link = item['item_link']
        salary_min = item['item_salary'][0]
        salary_max = item['item_salary'][1]
        salary_curr = item['item_salary'][2]
        vacancy_source = item['item_source']
        vacancy = {'vacancy_name': vacancy_name, 'vacancy_link': vacancy_link, 'salary_min': salary_min,
                   'salary_max': salary_max, 'salary_curr': salary_curr, 'vacancy_source': vacancy_source}
        collection.insert_one(vacancy)
        return item

    def salary_hh(self, salary):
        salary_min = None
        salary_max = None
        salary_curr = None
        for i in range(len(salary)):
            salary[i] = salary[i].replace('\xa0', '')
        if salary[0] == 'до':
            salary_max = float(salary[1])
            salary_curr = salary[3]
        elif salary[0] == 'от':
            salary_min = float(salary[1])
            salary_curr = salary[3]
        elif len(salary) == 7:
            salary_min = float(salary[1])
            salary_max = float(salary[2])
            salary_curr = salary[5]
        salary_finalized = [salary_min, salary_max, salary_curr]
        return salary_finalized

    def salary_sjru(self, salary):
        salary_min = None
        salary_max = None
        salary_curr = None
        for i in range(len(salary)):
            salary[i] = salary[i].replace('\xa0', '')
        if salary[0] == 'до':
            salary_max = float(salary[2].replace('руб', ''))
            salary_curr = salary[2][-4]
        elif salary[0] == 'от':
            salary_min = float(salary[2].replace('руб', ''))
            salary_curr = salary[2][-4]
        elif len(salary) == 7:
            salary_min = float(salary[0])
            salary_max = float(salary[4])
            salary_curr = salary[6]
        salary_finalized = [salary_min, salary_max, salary_curr]
        return salary_finalized
