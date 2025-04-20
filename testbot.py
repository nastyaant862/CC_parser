import telebot
from telebot import types #служит для создания кнопок

bot = telebot.TeleBot('6618174909:AAGdvPe3cC9vORvalMEh5-LiRewmDeGpabE')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Вас приветствует бот, с помощью которого вы можете оставить '
                                      'своё объявление о продаже или обмене билета на импромероприятие. '
                                      'Выберите нужное действие в списке команд ниже, оставьте объявление, '
                                      'и наши модераторы в ближайшее время его проверят и опубликуют.\n'
                                      '\n'
                                      'Спасибо, что выбрали наш <a href="https://t.me/improbilet">телеграм-канал</a>!\n'
                                      '\n'
                                      '/help - для просмотра команд бота', parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    markup = types.InlineKeyboardMarkup()
    buttonSell = types.InlineKeyboardButton(text="Хочу продать билет", callback_data="/sellticket")
    buttonSwap = types.InlineKeyboardButton(text="Хочу обменять билет", callback_data="/swap")
    buttonReport = types.InlineKeyboardButton(text="Хочу сообщить о мошенничестве", callback_data="/report")

    markup.row(buttonSell)
    markup.row(buttonSwap)
    markup.row(buttonReport)
    bot.send_message(message.chat.id, "/sellticket - продать билет\n"
                                      "/buyticket - купить билет\n"
                                      "/swap - обменять билет\n"
                                      "/report - сообщить о мошенничестве\n", reply_markup=markup)


# функция запустится, когда пользователь нажмет на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "/sellticket":
            sellticket(call.message)
            # bot.send_message(call.message.chat.id, "/sellticket")
        if call.data == "/swap":
            swap(call.message)
        if call.data == "/report":
            report(call.message)


@bot.message_handler(commands=['sellticket'])
def sellticket(message):
    bot.send_message(message.chat.id, "Напишите объявление о продаже по шаблону")


@bot.message_handler(commands=['swap'])
def swap(message):
    bot.send_message(message.chat.id, "Напишите объявление об обмене по шаблону")


@bot.message_handler(commands=['report'])
def report(message):
    bot.send_message(message.chat.id, "Расскажите, что случилось")


#@bot.message_handlers(content_types=["text"])


bot.polling(none_stop=True)
# bot.infinity_polling(none_stop=True)
