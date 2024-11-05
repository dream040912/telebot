import telebot
from setting import *

bot = telebot.TeleBot(token)

if __name__ == "__main__":
    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(message.chat.id, "Бот работает")


    @bot.message_handler(commands=["message"])
    def start(message):
        bot.send_message(message.chat.id, f'{message}')


    @bot.message_handler(commands=["sum"])
    def summ(message):
        text = message.text[4:]
        text = text.strip()
        text = text.split(" ")

        bot.send_message(message.chat.id, f"{int(text[0]) + int(text[1])}")


    @bot.message_handler(commands=["minus"])
    def minnus(message):
        text1 = message.text[6:]
        text1 = text1.strip()
        text1 = text1.split(" ")

        bot.send_message(message.chat.id, f"{int(text1[0]) - int(text1[1])}")


    @bot.message_handler(commands=["delit"])
    def dellit(message):
        text2 = message.text[6:]
        text2 = text2.strip()
        text2 = text2.split(" ")

        bot.send_message(message.chat.id, f"{int(text2[0]) / int(text2[1])}")


    bot.polling(none_stop=True)
