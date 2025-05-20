import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from peewee import IntegrityError

from tables import Games  # Ваша модель Peewee


def parse_price(price_str):
    """
    Преобразует цену из строки вида '1 234 ₽' или 'Free' в float.
    Если цена отсутствует или 'Free', возвращает 0.0.
    """
    if not price_str:
        return 0.0
    # Удаляем неразрывные пробелы, пробелы, символы валюты
    price_str = price_str.replace('\xa0', '').replace('₽', '').replace(',', '.').replace(' ', '').strip()
    if price_str.lower() in ('free', '', '-', 'бесплатно'):
        return 0.0
    try:
        return float(price_str)
    except ValueError:
        return 0.0


def parsing_steam():
    agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    edge_options = Options()
    edge_options.add_argument(f"user-agent={agent}")
    edge_options.add_argument("--headless")  # Запуск браузера без GUI
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")

    driver = webdriver.Edge(options=edge_options)
    try:
        driver.get("https://store.steampowered.com/search/?term=")

        # Скроллим страницу, чтобы подгрузить больше игр
        for _ in range(30):
            driver.execute_script("window.scrollBy(0, 2000)")
            time.sleep(0.5)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        games = soup.find_all("div", class_="responsive_search_name_combined")

        for current_game in games:
            try:
                title = current_game.find("span", class_="title").text.strip()

                # Сначала пытаемся получить цену со скидкой
                price_tag = current_game.find("div", class_="discount_final_price")
                if price_tag and price_tag.text.strip():
                    price_text = price_tag.text.strip()
                else:
                    # Если скидки нет — берем обычную цену
                    price_tag = current_game.find("div", class_="search_price")
                    if price_tag and price_tag.text.strip():
                        # Иногда там может быть старая цена и новая, берем последнюю часть
                        price_text = price_tag.get_text(separator=' ').strip().split()[-1]
                    else:
                        price_text = ""

                # Отладочный вывод, чтобы видеть что парсим
                print(f"Raw price text for '{title}': '{price_text}'")

                price = parse_price(price_text)

                # Получаем ссылку на игру
                link_tag = current_game.find_previous("a", href=True)
                link = link_tag['href'] if link_tag else ""

                # Создаем или обновляем запись в базе
                game, created = Games.get_or_create(name_game=title, defaults={
                    'price_game': price,
                    'link': link,
                    'sells': None,
                    'sells_price': None
                })

                if not created:
                    updated = False
                    if game.price_game != price:
                        game.price_game = price
                        updated = True
                    if game.link != link:
                        game.link = link
                        updated = True
                    if updated:
                        game.save()

                print(f"{title} | Цена: {price} | Ссылка: {link}")

            except Exception as e:
                print(f"Ошибка при обработке игры '{title if 'title' in locals() else 'Unknown'}': {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    parsing_steam()
