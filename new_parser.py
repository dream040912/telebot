import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from peewee import IntegrityError

from tables import Games  # ваша модель Peewee

def parse_price(price_str):
    """
    Преобразует цену из строки вида '1 234 ₽' или 'Free' в float.
    Если цена отсутствует или 'Free', возвращает 0.0.
    """
    price_str = price_str.replace('₽', '').replace(',', '.').replace(' ', '').strip()
    if price_str.lower() in ('free', '', '-'):
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
    edge_options.add_argument("--headless")  # Запуск без открытия окна браузера
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")

    driver = webdriver.Edge(options=edge_options)
    try:
        driver.get("https://store.steampowered.com/search/?term=")

        # Скроллим страницу для подгрузки игр
        for _ in range(30):
            driver.execute_script("window.scrollBy(0, 2000)")
            time.sleep(0.5)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        games = soup.find_all("div", class_="responsive_search_name_combined")

        for current_game in games:
            try:
                title = current_game.find("span", class_="title").text.strip()

                # Цена после скидки или обычная цена
                price_tag = current_game.find("div", class_="discount_final_price")
                if price_tag:
                    price_text = price_tag.text.strip()
                else:
                    # Если скидки нет, цена может быть в другом теге
                    price_text = current_game.find("div", class_="search_price").text.strip()

                price = parse_price(price_text)

                # Ссылка на игру
                link_tag = current_game.find_previous("a", href=True)
                link = link_tag['href'] if link_tag else ""

                # Проверяем, есть ли игра в базе
                game, created = Games.get_or_create(name_game=title, defaults={
                    'price_game': price,
                    'link': link,
                    'sells': None,
                    'sells_price': None
                })

                if not created:
                    # Обновляем цену и ссылку, если изменились
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
                print(f"Ошибка при обработке игры: {e}")
    finally:
        driver.quit()


parsing_steam()
