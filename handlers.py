import telebot
from settings import token
from telebot import types
from function import *

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Анализ Steam")
    item2 = types.KeyboardButton("Анализ DNS")
    item3 = types.KeyboardButton("Анализ Avito")

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "Привет!!! Для какого сайта нужен анализ???", reply_markup=markup)


@bot.message_handler(commands=["steam"])
def lissen(message):
    bot.send_message(message.chat.id, "Секунду...")
    list_game = get_games()
    for s in list_game:
        bot.send_message(message.chat.id, s)


@bot.message_handler(commands=["steam_discount"])
def discount(message):
    bot.send_message(message.chat.id, )
