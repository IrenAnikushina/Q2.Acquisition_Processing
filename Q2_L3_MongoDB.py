"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
записывающую собранные вакансии в созданную БД.
"""
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['vacancy_parser']

# https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=python

main_link = 'https://hh.ru'

search_criteria = input('Please enter profession, position, company name: ')

params = {'clusters': 'true',
          'enable_snippets': 'true',
          'salary': '',
          'st': 'searchVacancy',
          'text': search_criteria
          }

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                         '86.0.4240.183 Safari/537.36'}

result = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
if result.status_code != 200:
    print(f'ERROR! Please check the error type and remove the reason: {result.status_code}')
else:
    dom = bs(result.text, 'html.parser')
    page_block = dom.find('div', {'data-qa': 'pager-block'})
    if not page_block:
        last_page = 1
    else:
        last_page = int(page_block.find_all('a', {'class': 'HH-Pager-Control'})[-2].getText())
        print(f'last page {last_page}')
    # общий счетчик для вакансий после проверки на дубликаты
    total_y = 0
    total_n = 0
    for page in range(0, last_page):
        params['page'] = page
        result = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
        dom = bs(result.text, 'html.parser')
        vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item'})
        if len(vacancy_list) == 0:
            print(f'Vacancies with search criteria "{search_criteria}" were not found. Try to change search criteria')
        else:
            vacancies = []
            # переменные для счетчика
            y = 0
            n = 0
            for vacancy in vacancy_list:
                vacancy_data = {}
                profession_element = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})
                profession = profession_element.getText()
                profession_link = profession_element['href']
                employer_element = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
                try:
                    employer = employer_element.getText()
                except AttributeError:
                    employer = None
                try:
                    employer_link = main_link + employer_element['href']
                except TypeError:
                    employer_link = None
                city = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).getText()

                salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
                if not salary:
                    salary_min = None
                    salary_max = None
                    salary_currency = None
                else:
                    salary = salary.getText().replace('\xa0', '')
                    salary = re.split(' |-', salary)
                    try:
                        salary_currency = salary[2]
                    except IndexError:
                        salary_currency = salary[1]
                    if salary[0] == 'до':
                        salary_min = None
                        salary_max = int(salary[1])
                    elif salary[0] == 'от':
                        salary_min = int(salary[1])
                        salary_max = None
                    else:
                        salary_min = int(salary[0])
                        try:
                            salary_max = int(salary[1])
                        except ValueError:
                            salary_max = None

                vacancy_data['profession'] = profession
                vacancy_data['profession_link'] = profession_link
                vacancy_data['employer'] = employer
                vacancy_data['employer_link'] = employer_link
                vacancy_data['city'] = city
                vacancy_data['salary_min'] = salary_min
                vacancy_data['salary_max'] = salary_max
                vacancy_data['salary_currency'] = salary_currency
                # Для каждой ссылки на вакансию выполняется проверка на наличие в базе данных
                # После обработки всех страниц выводится счетчик - сколько всего добавлено, сколько отброшено
                for old_vacancy in db.vacancies.find({'profession_link': profession_link}):
                    n += 1
                    break
                else:
                    db.vacancies.insert_one(vacancy_data)
                    y += 1
            #    vacancies.append(vacancy_data)
            total_y += y
            total_n += n
            # вывод счетчика после обработки каждой страницы
            # print(f'New vacancy added: {y}, reentry cancelled: {n}')

    # итоговый счетчик
    print(f'New vacancies were added: {total_y}, reentry cancelled: {total_n}')

# скрин полученной БД приложила к файлу со скриптом

"""
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
"""
user_salary = int(input('Please input your expectations for salary: '))
for vacancy in db.vacancies.find({'$or': [{'salary_min': {'$gt': user_salary}}, {'salary_max': {'$gt': user_salary}}]}):
    pprint(vacancy)


"""
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
"""
# скрипт приведен выше - добавила проверку сразу по ходу формирования базы


