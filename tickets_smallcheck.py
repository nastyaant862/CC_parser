import datetime
import requests
import telebot

#token = '6618174909:AAGdvPe3cC9vORvalMEh5-LiRewmDeGpabE'
#bot = telebot.TeleBot(token)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

dt = datetime.datetime.now()
output = 'Проверка началась в {0:%H:%M} - {0:%d.%m.%Y}\n\n'.format(dt)

url = 'https://iframeab-pre4791.intickets.ru/seance/14771518'
res = requests.get(url, headers = headers)
code = res.status_code
if code == 200:
	output += f'✅ УСПЕШНО: ✅ {url}\n'
elif code == 404:
	output += f'Ничего не найдено\n'
else:
	output += f'Требуется проверка вручную: {url}\n'

print(output)

#bot.send_message(-1001545351085, output, disable_web_page_preview = True)