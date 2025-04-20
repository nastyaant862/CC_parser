# import requests
#
# res1 = requests.get('https://iframeab-pre5814.intickets.ru/events')
# res2 = requests.get('https://iframeab-pre4791.intickets.ru/events')
# print(res1.status_code)
# # print(res1.headers)
# # print(res1.text)
# print(res2.links)
#
# # file1 = open('C:\\Users\\Настя\\OneDrive\\Desktop\\test\\5814.txt', 'r+', encoding="utf-8")
# # file1.write(res1.text)
# #
# # file2 = open('C:\\Users\\Настя\\OneDrive\\Desktop\\test\\4791.txt', 'r+', encoding="utf-8")
# # file2.write(res2.text)

# from selenium import webdriver
# driver = webdriver.Chrome()
# # driver.get("https://iframeab-pre4791.intickets.ru/events")
# driver.get('https://iframeab-pre5814.intickets.ru/seance/13811418') #проверка
# if driver.title == "Intickets":
#     print('Good')
# else:
#     print("Bad")
# driver.quit()

import datetime
import time
import requests
import telebot

from selenium import webdriver
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

url = 'https://iframeab-pre4791.intickets.ru/events' # питерские - для теста, ШИШ - ЦЕЛЬ
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
flag = False
for c in cards:
    title = c.find('h2')
    if title.text.strip() == 'Черный StandUp. Большой концерт':
        #print(c)
        #driver.find_element(By.XPATH, '//h2[@title="'+ title.text.strip() +'"]').click()
        driver.find_element(By.XPATH, '//h2[@title="Черный StandUp. Большой концерт"]').click()
        necessary_url = driver.current_url
        output += f'✅ УСПЕШНО: ✅ {necessary_url}\n'
        flag = True
if flag == False:
    output += 'ШИШа пока нет'
print(output)

driver.quit()
# flag = False
# driver.find_element(By.CLASS_NAME, 'card-content').click()
# c = soup.find('div', class_='breadcrumbs x14')
# title = c.find('span')
# if title.text.strip() == 'Вечеринка Central Standuo':
#     necessary_url = driver.current_url
#     output += f'✅ УСПЕШНО: ✅ {necessary_url}\n'
#     flag = True
# if not flag:
#     output += 'ШИШа пока нет'
# print(output)


