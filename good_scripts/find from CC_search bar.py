from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import requests

options = Options()

# Отключаем ненужное
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.stylesheets": 2,
    "profile.managed_default_content_settings.media_stream": 2,
    "profile.managed_default_content_settings.plugins": 2,
    "profile.managed_default_content_settings.popups": 2,
}
options.add_experimental_option("prefs", prefs)

# Headless + оптимизация
#options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--remote-debugging-port=9222')
#options.add_argument('--user-data-dir=/tmp/chrome-profile')
options.add_argument('--disable-blink-features=AutomationControlled')

# Запуск
browser = webdriver.Chrome(options=options)

text = "Минск"

try:
    browser.get("https://comedyconcert.ru/")
    wait = WebDriverWait(browser, 3)
    main_tab = browser.current_window_handle  # сохраняем основную вкладку

    # Проверка и закрытие всплывающего окна
    try:
        popup = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.marquiz__bg.marquiz__bg_open')))
        print("Всплывающее окно обнаружено!")
        close_btn = wait.until(EC.element_to_be_clickable((By.ID, 'marquiz__close')))
        close_btn.click()
        print("Кнопка закрытия нажата.")
    except TimeoutException:
        print("Всплывающее окно не появилось — идём дальше.")

    urls = []

    for i in range(10):  # допустим, максимум 10 результатов
        try:
            # Ждем, пока модальное окно исчезнет, если оно ещё активно
            try:
                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.modal.active')))
            except TimeoutException:
                print("Модалка не исчезла, пробуем кликнуть по фону...")
                try:
                    # Кликаем в пустое место модального окна
                    backdrop = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.modal.active')))
                    backdrop.click()
                    print("Клик по фону выполнен.")
                    time.sleep(1)  # ждём закрытия
                except Exception as e:
                    print(f"Не удалось кликнуть по фону: {e}")

            # Клик по иконке поиска
            search_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.icon.searching__icon')))
            search_icon.click()

            # Ввод текста в поисковую строку
            search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.modal.active input')))
            search_input.clear()
            for char in text:
                search_input.send_keys(char)
                time.sleep(0.1)

            # Ожидание появления всех результатов
            search_results = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'div.header__search__overlay__example > ul > li')
            ))

            if i >= len(search_results):
                print("Достигнут конец списка.")
                break

            # Получаем ссылку и открываем в новой вкладке
            search_results[i].click()
            time.sleep(1)  # даем странице прогрузиться
            url = browser.current_url

            #browser.execute_script("window.open(arguments[0], '_blank');", url)
            #browser.switch_to.window(browser.window_handles[-1])  # переходим на новую вкладку

            # Ждем загрузки контента страницы
            #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.page-content')))
            # print(f"[{i}] URL: {url}")
            # urls.append(url)

            # Закрываем текущую вкладку
            #browser.close()

            # Возвращаемся на основную вкладку
            browser.switch_to.window(main_tab)

        except Exception as e:
            print(f"Ошибка при обработке элемента {i}: {e}")
            browser.switch_to.window(main_tab)  # на всякий случай возвращаемся
            continue

    print("\nСобираем ссылки с 'Минск' из /json...")
    urls = []
    tabs = requests.get("http://localhost:9222/json").json()
    for tab in tabs:
        title = tab.get("title", "")
        url = tab.get("url", "")
        if text.lower() in title.lower():
            urls.append(url)
            print(f"✅ Найдено: {title} -> {url}")

    print("\nСобранные ссылки:")
    for link in urls:
        print(link)

finally:
    input("Нажми Enter, чтобы закрыть браузер...")
    browser.quit()
