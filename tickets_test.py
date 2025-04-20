import datetime
import time
import requests
import telebot

from selenium import webdriver;
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

token = '6618174909:AAGdvPe3cC9vORvalMEh5-LiRewmDeGpabE'
bot = telebot.TeleBot(token)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

options = Options()
options.add_argument('--headless')
#options.add_argument('window-size=380,850')
options.add_argument('window-size=1920,1080')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9222')
driver = webdriver.Chrome(options=options)

dt = datetime.datetime.now()
output = 'Проверка началась в {0:%H:%M} - {0:%d.%m.%Y}\n\n'.format(dt)

#url = 'https://iframeab-pre7308.intickets.ru/events' # отключен виджет - для теста
#url = 'https://iframeab-pre7305.intickets.ru/events' # зетники - для теста
url = 'https://iframeab-pre4791.intickets.ru/events' # питерские - для теста
#url = 'https://iframeab-pre5814.intickets.ru/events' # истории и неигры - ЦЕЛЬ
#url = 'https://iframeab-pre5814.intickets.ru/seance/13811418' #проверка
driver.get(url)

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

soup = BeautifulSoup(driver.page_source, 'html.parser')

cards = soup.find_all('div', class_='card-content')

for c in cards:
    title = c.find('h2')
    print(title.text.strip())

driver.quit()