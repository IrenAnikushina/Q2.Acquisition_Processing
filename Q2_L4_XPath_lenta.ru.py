"""
Написать приложение, которое собирает основные новости с lenta.ru.
Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
Сложить собранные данные в БД
"""
from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
main_link = 'https://lenta.ru/'

response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)

news = dom.xpath('//time[@class="g-time"]/..')
news_list = []

for element in news:
    element_news = {}
    source = 'https://lenta.ru/'
    title = element.xpath('.//time[@class="g-time"]/../text()')
    link = element.xpath('.//time[@class="g-time"]/../@href')
    date = element.xpath('.//time[@class="g-time"]/@datetime')

    element_news['source'] = source
    element_news['title'] = title[0].replace('\xa0', ' ')
    element_news['link'] = source + link[0]
    element_news['date'] = date

    news_list.append(element_news)

pprint(news_list)

client = MongoClient('127.0.0.1', 27017)
db = client['lenta_ru_news_list']
news_collection = db.news_collection
news_collection.insert_many(news_list)


