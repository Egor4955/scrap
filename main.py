import requests
from bs4 import BeautifulSoup
import fake_headers
from unicodedata import normalize
import json

url = 'https://spb.hh.ru/search/vacancy?text=python+django+flask&salary=&ored_clusters=true&area=2&area=1'
headers_gen = fake_headers.Headers(browser='firefox', os='win')
response = requests.get(url, headers=headers_gen.generate())

html = response.text
soup = BeautifulSoup(html, 'html.parser')
div_serp = soup.find_all('div', class_="vacancy-serp-item__layout")
div_serp_list= []
for vacancy in div_serp:
    vacancy_link = vacancy.find('a', class_= 'serp-item__title')['href']
    vacancy_name = (vacancy.find('a', class_= 'serp-item__title')).text
    vacancy_city = vacancy.find(attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0]
    vacancy_company = (vacancy.find(attrs ={'data-qa': 'vacancy-serp__vacancy-employer'})).text
    vacancy_salary = vacancy.find('span', class_='bloko-header-section-2')
    if vacancy_salary is None:
        vacancy_salary = 'Не указано'
    else: vacancy_salary = vacancy_salary.text
    div_serp_list.append({
        'name': normalize('NFKD',vacancy_name),
        'link': normalize('NFKD',vacancy_link),
        'city': normalize('NFKD', vacancy_city),
        'company': normalize('NFKD', vacancy_company),
        'salary': normalize('NFKD',vacancy_salary)
    })

with open('vacancy_info.json', 'w', encoding="utf-8" ) as file:
    file.write(json.dumps(div_serp_list, indent=2, ensure_ascii=False))











