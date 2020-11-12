"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов
Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
* Наименование вакансии.
* Предлагаемую зарплату (отдельно минимальную, максимальную и валюту).
* Ссылку на саму вакансию.
* Сайт, откуда собрана вакансия.

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.
"""
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re

# https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=python

main_link = 'https://hh.ru'

search_criteria = input('Please enter profession, position, company name: ')
# start_page = 0

params = {'clusters': 'true',
          'enable_snippets': 'true',
          'salary': '',
          'st': 'searchVacancy',
          'text': search_criteria  # ,
          # 'page': start_page
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

    for page in range(0, last_page):
        params['page'] = page
        result = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
        dom = bs(result.text, 'html.parser')
        vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item'})
        if len(vacancy_list) == 0:
            print(f'Vacancies with search criteria "{search_criteria}" were not found. Try to change search criteria')
        else:
            vacancies = []
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
                    print(salary)
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

                vacancies.append(vacancy_data)

            pprint(vacancies)
