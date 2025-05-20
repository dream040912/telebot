import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from peewee import IntegrityError

from tables import Games  # Ваша модель Peewee


def parse_price_to_float(price_str):
    """
    Преобразует строку с ценой в float.
    Удаляет пробелы, символы валюты и слова типа 'руб'.
    Возвращает float или None, если преобразование невозможно.
    """
    try:
        cleaned = price_str.lower().replace("руб", "").replace(" ", "").replace(",", ".").replace("$", "").replace("₽", "")
        return float(cleaned)
    except ValueError:
        return None


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

                # Получаем скидку в процентах, если есть
                discount_tag = current_game.find("div", class_="search_discount")
                if discount_tag and discount_tag.text.strip():
                    discount_percent = discount_tag.text.strip()  # Например: "-50%"
                else:
                    discount_percent = "0%"

                # Получаем цену со скидкой или обычную цену
                price_tag = current_game.find("div", class_="discount_final_price")
                if price_tag and price_tag.text.strip():
                    price_text = price_tag.text.strip()
                    price_value = parse_price_to_float(price_text)
                else:
                    price_tag = current_game.find("div", class_="search_price")
                    if price_tag and price_tag.text.strip():
                        # Иногда там может быть старая цена и новая, берем последнюю часть
                        price_text = price_tag.get_text(separator=' ').strip().split()[-1]
                        price_value = parse_price_to_float(price_text)
                    else:
                        price_text = ""
                        price_value = None

                print(f"Raw price text for '{title}': '{price_text}', discount: {discount_percent}")

                # Получаем ссылку на игру
                link_tag = current_game.find_previous("a", href=True)
                link = link_tag['href'] if link_tag else ""

                # Создаем или обновляем запись в базе
                game, created = Games.get_or_create(name_game=title, defaults={
                    'price_game': price_text,
                    'sells': discount_percent,
                    'sells_price': price_value,
                    'link': link
                })

                if not created:
                    updated = False
                    if game.price_game != price_text:
                        game.price_game = price_text
                        updated = True
                    if game.sells != discount_percent:
                        game.sells = discount_percent
                        updated = True
                    if game.sells_price != price_value:
                        game.sells_price = price_value
                        updated = True
                    if game.link != link:
                        game.link = link
                        updated = True
                    if updated:
                        game.save()

                print(f"{title} | Цена: {price_text} | Скидка: {discount_percent} | Ссылка: {link}")

            except Exception as e:
                print(f"Ошибка при обработке игры '{title if 'title' in locals() else 'Unknown'}': {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    parsing_steam()
