from bs4 import BeautifulSoup
import requests
import re
from re import sub
from decimal import Decimal
import io
from datetime import datetime
import pandas

# поиск в определённой зоне
url = 'https://iframeab-pre4791.intickets.ru/seance/14771519'
# делаем запрос и получаем html
html_text = requests.get(url).text
# используем парсер lxml
soup = BeautifulSoup(html_text, 'lxml')

titles = soup.find('div', class_='breadcrumbs x14-600')
# print(titles)
print(html_text.status_code)