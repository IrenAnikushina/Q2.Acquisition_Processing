"""
2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time
from pprint import pprint
import json

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')

# я нашла вот эту штуку, но так и не поняла как оттуда достать список словарей. Буду благодарна, если подскажите как
## top_sellers = driver.find_elements_by_xpath("//div[contains(text(), 'Хиты продаж')]/../../../../../script")

scroll_button = driver.find_element_by_xpath("//div[contains(text(), 'Хиты продаж')]/../../../..//a[contains(@class, 'next-btn')]")
links = []
bestsellers_list = []

while True:
    time.sleep(3)
    len1 = len(links)
    # print(f'len1 {len1}')
    bestsellers = driver.find_elements_by_xpath("//div[contains(text(), 'Хиты продаж')]/../../../..//a[contains(@class, 'sel-product-tile-title')]")
    product_spec = {}
    for bestseller in bestsellers:
        link = bestseller.get_attribute('href')
        # print(link)
        if link not in links:
            links.append(link)
            product_spec = {'item': bestseller.get_attribute('data-product-info')}
            bestsellers_list.append(product_spec)
        else:
            pass

    len2 = len(links)
    # print(f'len2 {len2}')
    if len1 != len2:
        scroll_button.click()
    else:
        print(f'В список добавлено {len2} товаров')
        break

pprint(bestsellers_list)

client = MongoClient('127.0.0.1', 27017)
db = client['Mvideo_bestsellers']
Mvideo_bestsellers = db.Mvideo_bestsellers
Mvideo_bestsellers.insert_many(bestsellers_list)

driver.quit()
