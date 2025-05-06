from tables import Games, Ads


def get_games():
    list_game = []
    for games in Games:
        list_game.append(f"{games.name_game} | {games.price_game}")

    return list_game


print(get_games())

def get_ads():
    list_game = []
    for ads in Ads:
        list_game.append(f"{ads.title_ad} | {ads.price_ad}")

    return list_game
