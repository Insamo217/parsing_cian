import requests
import csv
import lxml
import re
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

base_url = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p=2&region=1&room2=1'

# функция, которая вычленяет необходимые данные из одной квартиры
def cian_parce(href, headers):
    session = requests.Session()
    request = session.get(href, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('main', attrs={'data-name': 'OfferCardPage'})
        for div in divs:
            title = div.find('h1', attrs={'data-name': 'OfferTitle'}).text # Название объявленияя
            price = div.find('span', attrs={'itemprop': 'price'}).text # Цена квартиры
            metro = div.find('ul', attrs={'class': 'a10a3f92e9--undergrounds--2pop3'}).text # Метро
            total_area = div.find('div', attrs={'class': 'a10a3f92e9--info-text--2uhvD'}).text # Общая площадь
            repair = div.find('div', attrs={'data-name': 'GeneralInformation'}).text # Общая информация
            #before_price = div.find('div', attrs={'class': 'price_history_widget-history-wrapper-leXEYJne'}).text # Предыдущая цена
            #year_of_construction = div.find('div', attrs={'class': 'a10a3f92e9--value--38caj'}).text # Год постройки
            textlookfor = r"Вторичка"
            type_of_housing = re.findall(textlookfor, repair) # Тип жилья
            textlookfor = r"Дизайнерский"
            allresults = re.findall(textlookfor, repair) # Тип ремонта
            print(title)
            print(price)
            print(metro)
            print(total_area)
            print(type_of_housing, end='\n\n ')
    else:
        print('ERROR flat')

# функция, собирающая список ссылок на квартиры
def cian_parce_flats(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'class': 'c6e8ba5398--main-container--1FMpY'})
        for div in divs:
            #title = div.find('a', attrs={'class': 'c6e8ba5398--header--1fV2A'}).text 
            href = div.find('a', attrs={'class': 'c6e8ba5398--header--1fV2A'})['href']
            cian_parce(href, headers)
    else:
        print("ERROR flats")
                

cian_parce_flats(base_url, headers)