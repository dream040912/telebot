import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options

from tables import Games, Ads


def parsing_steam():
    global title, price
    agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 "
             "Safari/537.36")
    edge_options = Options()
    edge_options.add_argument(f"user-agent={agent}")

    driver = webdriver.Edge()
    driver.get(f"https://store.steampowered.com/search/?term")

    for i in range(30):
        driver.execute_script("window.scrollBy(0, 2000)")
        time.sleep(0.5)

    html = driver.page_source

    #response = requests.get(html)
    soup = BeautifulSoup(html, "html.parser")

    games = soup.find_all("div", class_="responsive_search_name_combined")

    for current_game in games:
        try:
            price = current_game.find("div", class_="discount_final_price").text.strip()
            title = current_game.find("span", class_="title").text.strip()
            if Games.get(Games.name_game == title):
                Games.get(Games.name_game == title).price_game = price

        except Games.DoesNotExist:
            price = current_game.find("div", class_="discount_final_price").text.strip()
            title = current_game.find("span", class_="title").text.strip()
            game = Games(name_game=title, price_game=price)
            game.save()

        except:
            pass
        print(title, price)


def discount_steam():
    global title, price
    agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 "
             "Safari/537.36")
    edge_options = Options()
    edge_options.add_argument(f"user-agent={agent}")

    driver = webdriver.Edge()

    driver.get(f"https://store.steampowered.com/search/?term=")

    for i in range(30):
        driver.execute_script("window.scrollBy(0, 2000)")
        time.sleep(0.5)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    discount_games = soup.find_all("div", class_="responsive_search_name_combined")

    for current_game in discount_games:
        try:
            discount_title = current_game.find("div", class_="col search_name ellipsis").text.strip()  #название игры
            discount_game = current_game.find("div", class_="discount_pct").text.strip()  #азмерн скижки на игру
            start_price_game = current_game.find("div", class_="discount_original_price") #цена игры до скидки
            if discount_game:
                final_price_game = current_game.find("div", class_="discount_final_price").text.strip() #цена игры после скидки
                print(discount_title, discount_game, start_price_game, final_price_game)
        except:
            pass


def parsing_avito():
    agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 "
             "Safari/537.36")
    edge_options = Options()
    edge_options.add_argument(f"user-agent={agent}")

    driver = webdriver.Edge()
    driver.get(f"https://www.avito.ru/moskva?cd=1&q=игровой+компьютер")

    for i in range(5):
        driver.execute_script("window.scrollBy(0, 2000)")
        time.sleep(0.5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    ads = soup.find_all("div",
                        class_="styles-module-theme-_IJ5n tokens-light-module-theme-bNBfB styles-module-theme-cCHWP")
    print(ads)

    for current_ad in ads:
        price = current_ad.find("span",
                                class_="styles-module-size_l-j3Csw styles-module-size_l_dense-JjSpL").text.strip()
        title = current_ad.find("div", class_="iva-item-titleStep-zichc iva-item-ivaItemRedesign-u3mVt").text.strip()
        if Ads.get(Ads.title_ad == title):
            Ads.get(Ads.title_ad == title).price_ad = price


discount_steam()
