import telebot
from telebot import types
from settings import token
from function import get_games  # предполагается, что эта функция возвращает список игр

bot = telebot.TeleBot(token)


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("Анализ Steam")
    item2 = types.KeyboardButton("Анализ DNS")
    item3 = types.KeyboardButton("Анализ Avito")
    item4 = types.KeyboardButton("Помощь")
    markup.add(item1, item2, item3, item4)
    return markup


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    text = ("Привет! Я бот для анализа сайтов.\n\n"
            "Выберите нужный вариант из меню или введите команду:\n"
            "/steam - показать список игр Steam\n"
            "/steam_discount - показать игры со скидками (если реализовано)\n"
            "/help - помощь по боту")
    bot.send_message(message.chat.id, text, reply_markup=main_menu())


@bot.message_handler(commands=["steam"])
def show_steam_games(message):
    bot.send_message(message.chat.id, "Секунду, получаю список игр...")
    list_game = get_games()
    if not list_game:
        bot.send_message(message.chat.id, "Список игр пуст.")
        return
    # Формируем красивый нумерованный список
    games_text = "\n".join(f"{i+1}. {game}" for i, game in enumerate(list_game))
    bot.send_message(message.chat.id, f"Список игр Steam:\n\n{games_text}")

    # Отправляем список в текстовом файле
    with open("steam_games.txt", "w", encoding="utf-8") as f:
        f.write(games_text)
    with open("steam_games.txt", "rb") as f:
        bot.send_document(message.chat.id, f)


@bot.message_handler(commands=["steam_discount"])
def show_steam_discount(message):
    # Заглушка, можно реализовать логику скидок
    bot.send_message(message.chat.id, "Функция показа скидок пока не реализована.")


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.lower()
    if text == "анализ steam":
        show_steam_games(message)
    elif text == "анализ dns":
        bot.send_message(message.chat.id, "Функция анализа DNS пока не реализована.")
    elif text == "анализ avito":
        bot.send_message(message.chat.id, "Функция анализа Avito пока не реализована.")
    elif text == "помощь":
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, "Я не понял команду. Воспользуйтесь меню или /help.")


if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
