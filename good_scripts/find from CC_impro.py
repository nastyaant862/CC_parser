import requests
from bs4 import BeautifulSoup
import datetime

url = "https://comedyconcert.ru"

dt = datetime.datetime.now()
print('Проверка началась в {0:%H:%M} - {0:%d.%m.%Y}\n'.format(dt))

# Отправка GET-запроса с пользовательским агентом, чтобы избежать редиректа на другую версию сайта
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Выполним запрос без редиректов
response = requests.get(url, headers=headers, allow_redirects=False)

# Проверим, был ли редирект
if response.status_code == 302:
    print("Произошел редирект, следуем по новому адресу:", response.headers["Location"])
    url = response.headers["Location"]

# Получаем контент страницы
response = requests.get(url, headers=headers)

# Теперь парсим страницу с помощью BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

keywords = ["импров", "improv", "истории", "шоу из шоу", "шастун", "попов", "матвиенко", "позов"]

cards = soup.find_all("div", class_="event__list__card")
#print(f"🔍 Найдено карточек: {len(cards)}")

events = []

for card in cards:
    try:
        title_tag = card.select_one("a.event__list__card__title")
        title = title_tag.get_text(strip=True) if title_tag else "—"

        # Фильтрация по ключевым словам
        if not any(keyword in title.lower() for keyword in keywords):
            continue  # если ни одно ключевое слово не найдено - пропускаем

        city_tag = card.select_one("div.event__list__card__playground_info__title.font-bold")
        city = city_tag.get_text(strip=True) if city_tag else "—"

        date_tag = card.select_one("div.event__list__card__date")
        time_tag = card.select_one("div.event__list__card__time_group")
        datetime = f"{date_tag.text.strip()} {time_tag.text.strip()}" if date_tag and time_tag else "—"

        link_tag = card.select_one("a.event__list__card__title")
        relative_link = link_tag.get("href") if link_tag else ""
        full_link = f"https://comedyconcert.ru{relative_link}" if relative_link else "—"

        events.append({
            "Название": title,
            "Город": city,
            "Дата и время": datetime,
            "Ссылка": full_link
        })
    except Exception as e:
        print("Ошибка при парсинге карточки:", e)

if not events:
    print("❌ Подходящие мероприятия не найдены.")
else:
    print(f'Найдено {len(events)} подходящих мероприятий.')
    for event in events:
        print(f"\n🎭 {event['Название']}")
        print(f"📍 Город: {event['Город']}")
        print(f"🕒 Время: {event['Дата и время']}")
        print(f"🔗 Ссылка: {event['Ссылка']}")
