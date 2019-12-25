import requests
import csv
import lxml
import re
from bs4 import BeautifulSoup as bs
import pickle, shelve
import socks
import socket
import time


socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket


base_url = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&foot_min=30&house_material%5B0%5D=1&house_material%5B1%5D=2&house_material%5B2%5D=3&house_material%5B3%5D=4&house_material%5B4%5D=6&house_material%5B5%5D=8&max_house_year=2019&maxfloor=100&maxfloorn=100&min_house_year=1950&minfloor=1&minfloorn=1&object_type%5B0%5D=1&offer_type=flat&only_foot=2&p=1&region=1&repair%5B0%5D=2&repair%5B1%5D=3&repair%5B2%5D=4&room2=1'

headers = {'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

# функция, которая вычленяет необходимые данные из одной квартиры
def cian_parce(href, headers):
    flats = []
    session = requests.Session()
    request = session.get(href, headers=headers)
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
            print('test')
            ##print(metro_time)
            ##print(area)
            ##print(floor)
            ##print(numb_of_floors)
            #print(total_area)
            #print(home)
            #print(repair)
            ##print(type_of_repair)
            ##print(year_of_const)
            ##print(type_of_house)

    else:
        print('ERROR')
    return flats

# функция, которая которая записывает данные по каждой квартире в csv файл
def files_writer(flats):
    with open ('cian_flats_p1_time18.csv', 'a', encoding='utf8') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название квартиры', 'Цена', 'Метро', 'Время до метро, мин.',
                         'Площадь квартиры', 'Этаж', 'Количество этажей', 'Тип Ремонта', 
                         'Год постройки', 'Тип дома'))
        for flat in flats:                
            a_pen.writerow((flat['title'], flat['price'], flat['metro_station'], flat['metro_time'],
                            flat['area'], flat['floor'], flat['numb_of_floors'], flat['type_of_repair'],
                            flat['year_of_const'], flat['type_of_house']))

# функция, собирающая список ссылок на квартиры
def cian_parce_flats(base_url, headers):
    num = 0
    #response = requests.get(base_url, timeout=(10, 0.01)) # таймаут на соединения, таймаут на чтение (в секундах)
    #try:
        #requests.post(base_url, headers, timeout=10)
    #except requests.exceptions.Timeout:
        #print ("Timeout occurred")
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'class': 'c6e8ba5398--main-container--1FMpY'})
        for div in divs:
            num += 1
            #title = div.find('a', attrs={'class': 'c6e8ba5398--header--1fV2A'}).text 
            href = div.find('a', attrs={'class': 'c6e8ba5398--header--1fV2A'})['href']
            print(num, ":", href)
            cian_parce(href, headers)
            flats = cian_parce(href, headers)
            files_writer(flats)
            time.sleep(20)
            
    else:
        print("ERROR flats")


# открываем законсервированный файл с url на каждую страницу поиска и подставляем url в цикл              
#f = open('links.dat','rb')
#dict = pickle.load(f)
#num_p = 0
#for base_url in dict:
   # num_p += 1
   # a = dict[base_url]
   # print ("Страница поиска-", num_p, end='\n ')
   # cian_parce_flats(a, headers)

    
cian_parce_flats(base_url, headers)