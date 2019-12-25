import requests
import csv
import lxml
import re
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

#https://www.cian.ru/sale/flat/220336403/
#https://www.cian.ru/sale/flat/221896242/
base_url = 'https://www.cian.ru/sale/flat/220336403/'

def cian_parce(base_url, headers):
    flats = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('main', attrs={'data-name': 'OfferCardPage'})
        for div in divs:
            try:
                title = div.find('h1', attrs={'data-name': 'OfferTitle'}).text # Название объявленияя
                price = div.find('span', attrs={'itemprop': 'price'}).text # Цена квартиры
                metro_info = div.find('ul', attrs={'class': 'a10a3f92e9--undergrounds--2pop3'}).text # Метро
                total_area = div.find('div', attrs={'class': 'a10a3f92e9--info-block--3hCay'}).text # Общая площадь
                repair = div.find('div', attrs={'data-name': 'GeneralInformation'}).text # Общая информация квартиры
                home = div.find('div', attrs={'class': 'a10a3f92e9--column--2oGBs'}).text # О доме
                # Станция метро
                pattern = r"^\w{,17}\s?\w{,17}\s?\w{,17}"
                metro_station = ('\n'.join(re.findall(pattern, metro_info))) 
                # Время до метро
                pattern = r"^\w{,17}\s?\w{,17}\s?\w{,17}\s⋅\s\s(\d{1,2})\sмин.+"
                metro_time = ('\n'.join(re.findall(pattern, metro_info))) 
                # Тип ремонта
                pattern = r"Дизайнерский|Евроремонт|Косметический"
                type_of_repair = ('\n'.join(re.findall(pattern, repair))) 
                # Год постройки
                pattern = r"\d{4}"
                year_of_const = ('\n'.join(re.findall(pattern, home))) 
                # Тип дома
                pattern = r"Монолитный|Кирпичный|Панельный|Блочный|Кирпично-монолитный|Сталинский"
                type_of_house = ('\n'.join(re.findall(pattern, home))) 
                # Площадь квартиры
                pattern = r"^\w+"
                area = ('\n'.join(re.findall(pattern, total_area))) 
                # Этаж
                pattern = r"(\d{,2})\sиз\s"
                floor = ('\n'.join(re.findall(pattern, total_area))) 
                # Количество этажей
                pattern = r"\sиз\s(\d{,3})Этаж"
                numb_of_floors = ('\n'.join(re.findall(pattern, total_area))) 

                flats.append({
                    'title': title,
                    'price': price,
                    'metro_station': metro_station,
                    'metro_time': metro_time,
                    'area': area,
                    'floor': floor,
                    'numb_of_floors': numb_of_floors,
                    'type_of_repair': type_of_repair,
                    'year_of_const': year_of_const,
                    'type_of_house': type_of_house
                })
            except:
                pass

        print(title)
        print(price)
        #print(metro_info)
        print(metro_station)
        print(metro_time)
        print(area)
        print(floor)
        print(numb_of_floors)
        #print(total_area)
        #print(home)
        #print(repair)
        print(type_of_repair)
        print(year_of_const)
        print(type_of_house)

    else:
        print('ERROR')
    return flats
#cian_parce(base_url, headers)

def files_writer(flats):
    with open ('cian_flats.csv', 'w', encoding='utf8') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название квартиры', 'Цена', 'Метро', 'Время до метро, мин.',
                         'Площадь квартиры', 'Этаж', 'Количество этажей', 'Тип Ремонта', 
                         'Год постройки', 'Тип дома'))
        for flat in flats:                
            a_pen.writerow((flat['title'], flat['price'], flat['metro_station'], flat['metro_time'],
                            flat['area'], flat['floor'], flat['numb_of_floors'], flat['type_of_repair'],
                            flat['year_of_const'], flat['type_of_house']))

flats = cian_parce(base_url, headers)
files_writer(flats)