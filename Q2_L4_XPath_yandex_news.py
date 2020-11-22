"""
Написать приложение, которое собирает основные новости с yandex-новости.
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
main_link = 'https://yandex.ru/news/'

response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)

news = dom.xpath("//a[contains(@href, 'index') and @class='news-card__link']")

news_list = []
for element in news:
    title = element.xpath(".//text()")
    link = element.xpath("./@href")
    time = element.xpath('..//span[@class="mg-card-source__time"]/text()')
    source_name = element.xpath('..//span[@class="mg-card-source__source"]//text()')

    element_news = {'source': main_link, 'link': link, 'source_name': source_name, 'title': title,
                    'time': time}

    news_list.append(element_news)

pprint(news_list)

client = MongoClient('127.0.0.1', 27017)
db = client['yandex_ru_news_list']
news_collection = db.news_collection
news_collection.insert_many(news_list)