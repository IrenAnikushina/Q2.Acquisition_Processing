"""
1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о
письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172
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

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://mail.ru/')

mail = driver.find_element_by_id('mailbox:login-input')
mail.send_keys('study.ai_172')
domain = driver.find_element_by_id('mailbox:domain')
domain_select = Select(domain)
domain_select.select_by_visible_text('@mail.ru')

try:
    insert_pass = driver.find_element_by_id('mailbox:submit-button')
    insert_pass.click()
except exceptions.NoSuchElementException:
    print('Mail login not found')

password = driver.find_element_by_id('mailbox:password-input')
password.send_keys('NextPassword172')
password.send_keys(Keys.ENTER)

letters_amount = 0

mail = WebDriverWait(driver, 20)
mail = mail.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'nav-folders')))
try:  # вытаскиваю количество писем во входящих для ограничения цикла скролла
    letters = driver.find_element_by_xpath("//a[@href='/inbox/']")
    letters_value = str(letters.get_attribute("title")).split(' ')
    print(f'Во входящем ящике {letters_value[1]} писем')
    letters_amount = int(letters_value[1])
except:
    print('Время ожидания вышло или произошла ошибка')

links = []
while len(links) <= letters_amount:
    time.sleep(3)
    actions = ActionChains(driver)
    current_links = driver.find_elements_by_xpath("//a[contains(@class, 'js-letter-list-item')]")
    for el in current_links:
        link = el.get_attribute('href')
        if link not in links:
            links.append(link)
        else:
            pass
    # pprint(links)
    # print(len(links))
    actions.move_to_element(current_links[-1])
    actions.perform()

letters_details = []
for link in links:
    print(link)
    letter = {}
    driver.get(link)
    time.sleep(3)  # пришлось добавить ожидние для подгрузки письма, т.к. возникала ошибка, что элемента нет на странице
    subject = driver.find_element_by_class_name('thread__subject').text
    sender = driver.find_element_by_class_name('letter-contact').text
    datetime_value = driver.find_element_by_class_name('letter__date').text
    try:
        text = driver.find_element_by_class_name('letter-body').text
    except:
        text = "Unreadable"
    letter = {'subject': subject, 'sender': sender, 'datetime_value': datetime_value, 'text': text}

    letters_details.append(letter)

pprint(letters_details)

client = MongoClient('127.0.0.1', 27017)
db = client['mail_ru_post']
letters_collection = db.letters_collection
letters_collection.insert_many(letters_details)

driver.quit()