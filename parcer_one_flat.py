import requests
import csv
import lxml
import re
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}


base_url_1 = 'https://www.cian.ru/sale/flat/220336403/'

base_url_2 = 'https://www.cian.ru/sale/flat/203985330/'

base_url_3 = 'https://www.cian.ru/sale/flat/223219491/'

flats = [base_url_1, base_url_2, base_url_3]


def cian_parce(base_url, headers):
    #flat = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('main', attrs={'data-name': 'OfferCardPage'})
        for div in divs:
            title = div.find('h1', attrs={'data-name': 'OfferTitle'}).text # Название объявленияя
            price = div.find('span', attrs={'itemprop': 'price'}).text # Цена квартиры
            metro = div.find('ul', attrs={'class': 'a10a3f92e9--undergrounds--2pop3'}).text # Метро
            total_area = div.find('div', attrs={'class': 'a10a3f92e9--info-text--2uhvD'}).text # Общая площадь
            repair = div.find('div', attrs={'data-name': 'GeneralInformation'}).text # Общая информация
            before_price = div.find('div', attrs={'class': 'price_history_widget-history-wrapper-leXEYJne'}).text # Предыдущая цена
            year_of_construction = div.find('div', attrs={'class': 'a10a3f92e9--value--38caj'}).text # Год постройки
            textlookfor = r"Вторичка"
            type_of_housing = re.findall(textlookfor, repair) # Тип жилья
            textlookfor = r"Дизайнерский"
            allresults = re.findall(textlookfor, repair) # Тип ремонта

            print(title)
            #print(year_of_construction)
            print(price)
            #print(before_price)
            print(metro)
            print(total_area)
            print(type_of_housing, end='\n\n ')
            #print(allresults)
    else:
        print('ERROR')

for flat in flats:
    cian_parce(flat, headers)

#def files_writer(jobs):
#    with open ('parased_jobs.csv', 'a') as file:
#        a_pen = csv.writer(file)
#        a_pen.writerow(('Название вакансии', 'URL', 'Название компании', 'Описание'))
#            for job in jobs:
#                a_pen.writerow((job['title'], job['href'], job['company'], job['content']))

#jobs = hh_parce(base_url, headers)
#files_writer(jobs)