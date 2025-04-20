import requests
from bs4 import BeautifulSoup
import datetime
import json
import os


def send_telegram_channel(message):
    token = '6618174909:AAGdvPe3cC9vORvalMEh5-LiRewmDeGpabE'
    chat_id = "-1002527661703"  # ID канала
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("❗️Ошибка отправки в канал:", response.text)


FILENAME = "events.json"


def load_previous_events():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_current_events(events):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)


def event_key(event):
    # Ключ, по которому можно сравнивать события
    return f"{event['Название']}|{event['Дата и время']}|{event['Ссылка']}"

# === Парсинг ===

url = "https://comedyconcert.ru"
dt = datetime.datetime.now()
message = 'Проверка в {0:%H:%M} — {0:%d.%m.%Y}\n\n'.format(dt)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers, allow_redirects=False)

if response.status_code == 302:
    print("Произошел редирект, следуем по новому адресу:", response.headers["Location"])
    url = response.headers["Location"]

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

keywords = ["импров", "improv", "истории", "шоу из шоу", "шастун", "попов", "матвиенко", "позов"]
cards = soup.find_all("div", class_="event__list__card")

events = []

for card in cards:
    try:
        title_tag = card.select_one("a.event__list__card__title")
        title = title_tag.get_text(strip=True) if title_tag else "—"

        if not any(keyword in title.lower() for keyword in keywords):
            continue

        city_tag = card.select_one("div.event__list__card__playground_info__title.font-bold")
        city = city_tag.get_text(strip=True) if city_tag else "—"

        date_tag = card.select_one("div.event__list__card__date")
        time_tag = card.select_one("div.event__list__card__time_group")
        datetime_str = f"{date_tag.text.strip()} {time_tag.text.strip()}" if date_tag and time_tag else "—"

        link_tag = card.select_one("a.event__list__card__title")
        relative_link = link_tag.get("href") if link_tag else ""
        full_link = f"https://comedyconcert.ru{relative_link}" if relative_link else "—"

        events.append({
            "Название": title,
            "Город": city,
            "Дата и время": datetime_str,
            "Ссылка": full_link
        })
    except Exception as e:
        print("Ошибка при парсинге карточки:", e)

# = Сравнение с предыдущими результатами =

previous_events = load_previous_events()
previous_keys = set(event_key(e) for e in previous_events)
current_keys = set(event_key(e) for e in events)

new_keys = current_keys - previous_keys
new_events = [e for e in events if event_key(e) in new_keys]

if new_events:
    print(f"\n✨ Найдено новых мероприятий: {len(new_events)}")
    for event in new_events:
        message += (
            f"<b>🎭 {event['Название']}</b>\n"
            f"📍 <b>{event['Город']}</b>\n"
            f"🕒 {event['Дата и время']}\n"
            f"🔗 <a href=\"{event['Ссылка']}\">Перейти к событию</a>"
            '\n\n'
        )
    send_telegram_channel(message)

else:
    message += "ℹ️ Не найдено новых мероприятий."
    send_telegram_channel(message)

# Обновляем файл
save_current_events(events)
