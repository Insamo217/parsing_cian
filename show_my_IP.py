from bs4 import BeautifulSoup
import requests
import socks
import socket
import time

def checkIP():
    ip = requests.get('http://checkip.dyndns.org').content
    soup = BeautifulSoup(ip, 'html.parser')
    print(soup.find('body').text)



# Current IP Address: 128.74.215.173 

socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket

for i in range(10):
    checkIP()
    time.sleep(11)