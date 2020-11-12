import requests
import json
from pprint import pprint

"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
"""
# документация: https://api.github.com/users/USERNAME/repos

link = 'https://api.github.com'
user_name = 'IrenAnikushina'
result = requests.get(f'{link}/users/{user_name}/repos')

print(f"Задание №1\nСписок репозиториев пользователя {user_name}:")
for i in result.json():
    print(i['name'])

with open('repo_list.json', 'w') as file:
    json.dump(result.json(), file)

"""
2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). 
Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. 
Ответ сервера записать в файл.
Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide). 
Сделайте запрос, чтб получить список всех сообществ на которые вы подписаны.
"""


url = "https://the-cocktail-db.p.rapidapi.com/popular.php"
headers = {
    'x-rapidapi-key': "f3e1f42c0fmsh0fb7dab38ae073ap1d1ab2jsn0d7b9c9787ae",
    'x-rapidapi-host': "the-cocktail-db.p.rapidapi.com"
    }
response = requests.get(url, headers=headers)
result = response.json()

print(f"\nЗадание №2\nTheCocktailDB TOP 20:")
n = 1
for i in result['drinks']:
    print(f"\nCocktail №{n} - {i['strDrink']}\nVisual presentation: {i['strDrinkThumb']}")
    n += 1

with open('famous_cocktails.json', 'w') as file:
    json.dump(response.json(), file)
