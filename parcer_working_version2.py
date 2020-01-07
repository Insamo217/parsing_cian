import requests
import csv
import lxml
import re
from bs4 import BeautifulSoup as bs
import pickle, shelve
import socks
import socket
import time

#браузер пользователя
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

#функция отображения текущего IP
def checkIP():
    ip = requests.get('http://checkip.dyndns.org').content
    soup = bs(ip, 'html.parser')
    print(soup.find('body').text)

#функция смены IP    
def change_IP():
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150) #замена IP
    socket.socket = socks.socksocket #замена IP
    time.sleep(11) #прописываем таймаут равный 11 сек

# функция, которая вычленяет необходимые данные из одного объявления
def cian_parce(href, headers):
    flats = []
    session = requests.Session() #запускаем сессию начала пользованя сайтом
    request = session.get(href, headers=headers) #отправляем запрос на сайт
    if request.status_code == 200: #если запрос положительный выполняется следующие операции
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('main', attrs={'data-name': 'OfferCardPage'}) #ищет дивы на странице
        if len(divs) == 0:
            raise Exception #принудительно вызывает ошибку если возникает капча (дивов на странице нет)
        for div in divs: #цикл на перебор значений в объявлении
            try:
                title = div.find('h1', attrs={'data-name': 'OfferTitle'}).text # Название объявленияя
                price_digit = div.find('span', attrs={'itemprop': 'price'}).text # Цена квартиры
                metro_info = div.find('ul', attrs={'class': 'a10a3f92e9--undergrounds--2pop3'}).text # Метро
                total_area = div.find('div', attrs={'class': 'a10a3f92e9--info-block--3hCay'}).text # Общая площадь
                repair = div.find('div', attrs={'data-name': 'GeneralInformation'}).text # Общая информация квартиры
                home = div.find('div', attrs={'class': 'a10a3f92e9--column--2oGBs'}).text # О доме
                district_info = div.find('address', attrs={'class': 'a10a3f92e9--address--140Ec'}).text # О доме
                # Перевод цены в числовой формат
                pattern = r"[^A-Za-z0-9]+"
                price = (re.sub(pattern, '', price_digit))
                # Район
                pattern = r"^\w+,\s\w+,\sр-н\s(\w{,17}\W?\w{,17}\s?\w{,17}),\s"
                district = ('\n'.join(re.findall(pattern, district_info))) 
                # Станция метро
                pattern = r"^\w{,17}\W?\w{,17}\s?\w{,17}"
                metro_station = ('\n'.join(re.findall(pattern, metro_info))) 
                # Время до метро
                pattern = r"^\w{,17}\W?\w{,17}\s?\w{,17}\s⋅\s\s(\d{1,2})\sмин.+"
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
                    'district': district,
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
           
            #вывод отображаемый информации при парсинге в терминал
            print(title)
            #print(price_digit)
            print(price)
            print(district)
            #print(metro_info)
            print(metro_station)
            #print(metro_time)
            #print(area)
            #print(floor)
            #print(numb_of_floors)
            #print(total_area)
            #print(home)
            #print(repair)
            #print(type_of_repair)
            #print(year_of_const)
            #print(type_of_house)

    else:
        print('ERROR') #если запрос отрицательный
    return flats

# функция, которая которая записывает данные из каждого объявления в csv файл
def files_writer(flats):
    with open ('cian_flats111.csv', 'a', encoding='utf8') as file:
        a_pen = csv.writer(file)
        #a_pen.writerow(('Название квартиры', 'Цена', 'Район', 'Метро', 'Время до метро, мин.',
                        # 'Площадь квартиры', 'Этаж', 'Количество этажей', 'Тип Ремонта', 
                         #'Год постройки', 'Тип дома'))
        for flat in flats:                
            a_pen.writerow((flat['title'], flat['price'], flat['district'], flat['metro_station'], flat['metro_time'],
                            flat['area'], flat['floor'], flat['numb_of_floors'], flat['type_of_repair'],
                            flat['year_of_const'], flat['type_of_house']))#запись в CSV

# функция, собирающая список ссылок на объявления
def cian_parce_flats(base_url, headers):
    hrefs = [] #добавляем список в котором будут ссылки на квартиры 
    num = 0 #добавляем нумерацию
    print('Обновление IP')
    change_IP()
    checkIP() #отображение IP
    session = requests.Session() #запуск новой сессии 
    request = session.get(base_url, headers=headers) #отправляем запрос на сайт
    if request.status_code == 200: #если запрос положительный выполняется следующие операции
        print("Ответ с сервера положительный")
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'class': 'c6e8ba5398--main-container--1FMpY'})
        while len(divs) == 0:#пока станица не отобразит список объявлений:
            print('Список квартир не получен, меняем IP')
            #checkIP() #печать IP
            change_IP() #смена IP
            checkIP()#отображение нового IP
            session = requests.Session() #запуск новой сессии 
            request = session.get(base_url, headers=headers) #отправляем запрос на сайт
            if request.status_code == 200: #если запрос положительный выполняется следующие операции
                print("Повторный ответ с сервера положительный")
                soup = bs(request.content, 'lxml')
                divs = soup.find_all('div', attrs={'class': 'c6e8ba5398--main-container--1FMpY'})
        if len(divs) != 0:
            print('Ссылки на объявления по текущей странице поиска')
        for div in divs:
            num += 1 #присвоение нумерации
            href = div.find('a', attrs={'class': 'c6e8ba5398--header--1fV2A'})['href'] #ссылка на объявление
            hrefs.append(href) #добавление в список новой ссылки на объявление
            print(num, ":", href) #печать номера и ссылки на объявление    
        href_n = 0 #вводит переменную на обозначение кол-во ссылок на объявления
        while href_n < len(hrefs): #если кол-во ссылок на объявления в терминале меньше кол-во ссылок с сайта, то
            try: #если сайт возвратил данные с объявления
                href = hrefs[href_n] #нумерация квартир из объявлений
                print("Квартира №", href_n)
                flats = cian_parce(href, headers) #печать в терминал инфо из объявления
                href_n += 1 #счетчик ссылок на объявления
                files_writer(flats)#запись данных с объявления в CSV
            except: #если возникла ошибка подсоединения - меняем IP
                print('Данные по квартире не получены, меняем IP')
                #checkIP() #печать IP
                change_IP()
                checkIP()#отображение нового IP
    else:
        print("ERROR flats")
            
#основная функция
def main():
    f = open('links_of_54_pages.dat','rb') # открываем законсервированный файл с url на каждую страницу поиска  
    dict_ = pickle.load(f)
    num_p = 0
    for base_url in dict_: #подставляем каждый новый URL в ф-цию собирающую ссылки на объявления 
        num_p += 1 
        a = dict_[base_url]
        print ("Страница поиска -", num_p, end='\n ')
        cian_parce_flats (a,headers)

main()