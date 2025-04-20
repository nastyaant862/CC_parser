import telebot
from telebot import types
import time
from datetime import datetime
from bs4 import BeautifulSoup

bot = telebot.TeleBot('7149335941:AAEZxSUpM4HZ5yXrNDEHuisIxP62wbfk7Ys')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Процент металла: 0\n", parse_mode='html')
    time.sleep(4)
    bot.send_message(message.chat.id, "Процент металла: 50\n", parse_mode='html')
    time.sleep(4)
    bot.send_message(message.chat.id, "Процент металла: 66.66\n", parse_mode='html')
    time.sleep(4)
    bot.send_message(message.chat.id, "Процент металла: 50\n", parse_mode='html')
    time.sleep(4)
    bot.send_message(message.chat.id, "Процент металла: 40\n", parse_mode='html')
    time.sleep(4)


bot.polling(none_stop=True)
