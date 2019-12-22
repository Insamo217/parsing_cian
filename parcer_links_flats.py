import requests
import csv
import lxml
import re
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}


base_url = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p=2&region=1&room2=1'


def cian_parce_flats(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'class': 'c6e8ba5398--main-container--1FMpY'})
        for div in divs:
            title = div.find('a', attrs={'class': 'c6e8ba5398--header--1fV2A'}).text 
            href = div.find('a', attrs={'class': 'c6e8ba5398--header--1fV2A'})['href']
            print(href)
            
    else:
        print("ERROR")

cian_parce_flats(base_url, headers)
           