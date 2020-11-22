"""
Написать приложение, которое собирает основные новости с news.mail.ru ###блок, котрый Вы обвели на уроке
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
main_link = 'https://news.mail.ru/'

response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)

links = dom.xpath('//div[contains(@class, "daynews__item")]//@href|//a[@class="list__text"]//@href')

news_list = []

for link in links:
    response = requests.get(link, headers=headers)
    dom = html.fromstring(response.text)
    title = dom.xpath("//h1[@class='hdr__inner']/text()")
    date = dom.xpath("//@datetime")
    source_name = dom.xpath("//span[@class='breadcrumbs__item']//span[@class='link__text']/text()")

    element_news = {'source': main_link, 'link': main_link + link, 'source_name': source_name, 'title': title,
                    'date': date}

    news_list.append(element_news)

pprint(news_list)

client = MongoClient('127.0.0.1', 27017)
db = client['mail_ru_news_list']
news_collection = db.news_collection
news_collection.insert_many(news_list)
