import telebot
from telebot import types
import datetime
from datetime import datetime
# import _mysql_connector

bot = telebot.TeleBot('6618174909:AAGdvPe3cC9vORvalMEh5-LiRewmDeGpabE')
form_url = ('https://docs.google.com/forms/d/e/1FAIpQLSeFn-eMMc64YQQr'
            'o55c4spn5lLx2obtKZHvHfBoknAZ9nhyiA/viewform?usp=sharing')
# 603778669
admins_id = [603778669] # заходим в админский режим
arr_days_week = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
arr_windows = [
    "ПН - 17:30",
    "ВТ - 18:00",
    "ЧТ - 15:00",
    "ВТ - 16:30"
]


def check_time(new2):
    new2_hour = new2.split(':')[0]
    new2_minute = new2.split(':')[1]
    if not new2_hour.isdigit() or not new2_minute.isdigit():  # проверка, числовая ли строка
        return 0
    else:
        if int(new2_hour) > 24 or int(new2_minute) > 59:
            return 0
        else:
            return 1


def sort_arr_windows_day(arr_windows):
    ind_j = 0
    ind_min = 0
    for i in range(len(arr_windows) - 1):
        index_min = i
        for j in range(i+1, len(arr_windows)):
            day_j = arr_windows[j].split()[0]
            day_ind_min = arr_windows[index_min].split()[0]
            for k in range(0, len(arr_days_week)):
                curr = arr_days_week[k]
                if curr == day_j:
                    ind_j = k
                if curr == day_ind_min:
                    ind_min = k
            if ind_j < ind_min:
                index_min = j
        arr_windows[i], arr_windows[index_min] = arr_windows[index_min], arr_windows[i]


def sort_arr_windows_time(arr_windows):
    for i in range(len(arr_windows) - 1):
        day_i = arr_windows[i].split()[0]
        day_i_1 = arr_windows[i+1].split()[0]
        if day_i == day_i_1:
            time_i = arr_windows[i].split()[2]
            time_i_1 = arr_windows[i+1].split()[2]

            time_i = datetime.strptime(time_i, '%H:%M')
            time_i_1 = datetime.strptime(time_i_1, '%H:%M')
            if time_i > time_i_1:
                arr_windows[i], arr_windows[i+1] = arr_windows[i+1], arr_windows[i]


@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in admins_id:  # администрирование
        markup = types.InlineKeyboardMarkup()
        button_show_my_windows = types.InlineKeyboardButton(text="Узнать мои окошки", callback_data="/show_my_windows")
        markup.row(button_show_my_windows)
        bot.send_message(message.chat.id, "<b>[режим администратора]</b>\n"
                                          "\n"
                                          "Вот, что можно сделать:", reply_markup=markup, parse_mode='html')

    else:
        bot.send_message(message.chat.id, 'Здравствуйте! Меня зовут Ангелина, и я репетитор по '
                                          'английскому, французскому и испанскому языку. '
                                          'С помощью этого бота вы можете оставить заявку '
                                          'на запись ко мне на занятия.\n'
                                          '\n'
                                          '/help_me — для просмотра команд бота.', parse_mode='html')


@bot.message_handler(commands=['help_me'])
def help_me(message):
    markup = types.InlineKeyboardMarkup()
    button_time = types.InlineKeyboardButton(text="Узнать мои окошки", callback_data="/windows")
    button_go = types.InlineKeyboardButton(text="Записаться", callback_data="/register")
    markup.row(button_time)
    markup.row(button_go)
    bot.send_message(message.chat.id, "Вот, что вы можете сделать:", reply_markup=markup)


@bot.message_handler(commands=['add_window'])
def add_window(message):
    bot.send_message(message.chat.id, "Добавьте окошко в формате: <b>ДН - ЧЧ:ММ</b>, где ДН - день недели (ПН, ВТ, СР и т.д.)",
                     parse_mode="html")
    bot.register_next_step_handler(message, process_text_add)


def process_text_add(message):
    new = message.text
    cnt_space = 0
    flag = 0
    for i in range(0, len(new), 1):
        if new[i] == ' ':
            cnt_space += 1
    if cnt_space == 2:
        new1 = new.split()[0]
        new2 = new.split()[2]
        if new1 not in arr_days_week:
            bot.send_message(message.chat.id,
                             "Ошибка, введите данные правильно [ДН - капсом]",
                             parse_mode="html")
            bot.register_next_step_handler(message, process_text_add)
            flag = 1
        if not check_time(new2):
            bot.send_message(message.chat.id,
                             "Ошибка, введите данные правильно [ошибка в введении времени]",
                             parse_mode="html")
            bot.register_next_step_handler(message, process_text_add)
            flag = 1
    else:
        bot.send_message(message.chat.id,
                         "Ошибка, введите данные правильно [не хватает пробелов]",
                         parse_mode="html")
        bot.register_next_step_handler(message, process_text_add)
        flag = 1
    if flag == 0:
        arr_windows.append(new)
        markup = types.InlineKeyboardMarkup()
        button_show_my_windows = types.InlineKeyboardButton(text="Узнать мои окошки", callback_data="/show_my_windows")
        markup.row(button_show_my_windows)
        bot.send_message(message.chat.id,"Окошко добавлено", parse_mode="html", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "/show_my_windows":
            sort_arr_windows_day(arr_windows)
            sort_arr_windows_time(arr_windows)

            list_of_windows = '<b>Список свободных окошек:</b> \n \n'
            for i in range(len(arr_windows)):
                list_of_windows += arr_windows[i] + '\n'

            markup = types.InlineKeyboardMarkup()
            button_edit_my_windows = types.InlineKeyboardButton(text="Изменить окошки", callback_data="/edit_my_windows")
            markup.row(button_edit_my_windows)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=list_of_windows, reply_markup=markup, parse_mode='html')

        elif call.data == "/edit_my_windows":
            markup = types.InlineKeyboardMarkup()
            button_add_window = types.InlineKeyboardButton(text="Добавить окошко", callback_data="/add_window")
            button_del_window = types.InlineKeyboardButton(text="Удалить окошко", callback_data="/del_my_windows")
            markup.row(button_add_window)
            markup.row(button_del_window)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Что сделать?", reply_markup=markup)

        elif call.data == "/add_window":
            add_window(call.message)

        elif call.data == "/register":
            markup = types.InlineKeyboardMarkup()
            reg_url_button = types.InlineKeyboardButton(text="URL", url=form_url)
            markup.row(reg_url_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Запись по ссылке:", reply_markup=markup)

        elif call.data == "/windows":
            sort_arr_windows_day(arr_windows)
            sort_arr_windows_time(arr_windows)

            list_of_windows = '<b>Список свободных окошек:</b> \n \n'
            for i in range(len(arr_windows)):
                list_of_windows += arr_windows[i] + '\n'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=list_of_windows, parse_mode='html')

        bot.answer_callback_query(call.id)


bot.polling(none_stop=True)
