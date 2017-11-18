# -*- coding: utf-8 -*-
from app import app
from app.config import token #Забираем токен из config.py (Этот файл содержит переменную token c занчением, выдаваемым botfather в telegram)
from app.db_postgresql import SQL_Postgre
from app.csvEditor import csv_dict_reader
from app.ExchangeRates import current_exchange_rate
import os
import telebot
from flask import request
from app.timezone import get_utc_offset_timezone, get_time_from_another_timezone
import requests
import datetime
import time
import threading
import shelve


bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Можно так
    # user = bot.get_me().__dict__['first_name']
    # Или так
    botName = bot.get_me().first_name # Берем имя бота
    userName = message.from_user.first_name # Берем имя пользователя
    chat_id = message.chat.id
    # Приветсвие



    '''
    Валидация клиента в системе
    '''

    # Получаем данные
    userId = message.from_user.id # id пользователя в telegram
    # Являетеся ли ботом? В документации есть is_bot
    firstName = message.from_user.first_name # Имя пользователя
    userName = message.from_user.username # Имя, отображающееся в telegram
    lastName = message.from_user.last_name # Фамилия пользователя
    languageCode = message.from_user.language_code # Используемый язык
    msg_date = message.date #Дата отправки /start

    db = SQL_Postgre()
    # check_user_availible = True - Пользователь существует в системе
    #                      = False - Пользователь не существует в системе
    check_user_availible = db.check_user_id(userId)
    if check_user_availible == False:
        curr_utc_time = datetime.datetime.utcnow()
        timezone = get_utc_offset_timezone(curr_utc_time, msg_date)
        a = db.new_user(userId,firstName,userName,lastName,timezone)

        # После регистрации клиента в системе выводим первое приветсвие
        """
        bot.send_message(message.chat.id, userName + ", Приветствую! Меня зовут " + botName + ". Я ваша персональная помощница.\nПодпишитесь на мои сервисы и каждое утро вы будете получать уведомления.")
        list_subscriptions = "Чтобы подписаться на сервис, нажмите на него или напишите мне: \n/time - дата и время\n/weather - погода на сегодня\n/currency - курс валют\n/contact - уведомления о днях рождения"
        bot.send_message(message.chat.id, list_subscriptions)
        list_commands = "Также вы можете воспользоваться командами: \n/time - Текущее время\n/contacts - Управление контактами\n/currency - курс валют"
        bot.send_message(message.chat.id, list_commands)
        """
        bot.send_message(message.chat.id, userName + ", Приветствую! Меня зовут " + botName + ". Чем я могу помочь?")
        list_subscriptions = "/currentSubscriptions - текущие подписки"
        bot.send_message(message.chat.id, list_subscriptions)
        list_commands = "Список команд: \n/time - Текущее время\n/contacts - Управление контактами\n/currency - курс валют"
        bot.send_message(message.chat.id, list_commands)
    else:
        bot.send_message(message.chat.id, userName + ", Приветствую! Меня зовут " + botName + ". Чем я могу помочь?")
        list_subscriptions = "/currentSubscriptions - текущие подписки"
        bot.send_message(message.chat.id, list_subscriptions)
        list_commands = "Список команд: \n/time - Текущее время\n/contacts - Управление контактами\n/currency - курс валют"
        bot.send_message(message.chat.id, list_commands)

    db.close()

@bot.message_handler(commands=['time'])
def send_time_now(message):
    currDTime = datetime.datetime.fromtimestamp(message.date)
    bot.send_message(message.chat.id, 'Сегодня {:%d %b %Y, %H:%M } '.format(currDTime))

@bot.message_handler(commands=['contacts'])
def send_welcome_contacts(message):
    bot.send_message(message.chat.id, "Список команд:\n /createContact - Загрузить контакты файлом")
    storage = shelve.open('shelve')
    storage[str(message.chat.id)] = 'init'
    storage.close()

@bot.message_handler(func=lambda message: True, commands=['createContact'])
def new_contact_list(message):
    chat_id = message.chat.id
    with shelve.open('shelve') as storage:
        if storage.get(str(chat_id)) != None:
            state = storage[str(chat_id)]
            if 'init' in state:
                bot.send_message(message.chat.id, 'Пожалуйста, загрузите файл в формате GOOGLE CSV\nПодробнее: https://www.google.com/contacts/u/0/?cplus=0#contacts\nЕще->Экспорт->Выберите формат файла для экспорта->\
                                                                       Google CSV (для импорта в аккаунт Google)')


        storage.clear()
        storage.close()


# Загрузка документа
@bot.message_handler(content_types=['document'])
def downloadFile(message):
    userId = message.from_user.id
    a = message.document.file_id
    file_info = bot.get_file(a)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    csv_dict_reader(file.text, userId)
    bot.send_message(message.chat.id, "Файл успешно загружен.")

@bot.message_handler(commands=['currency'])
def send_exchange_rates(message):
    dollar,euro = current_exchange_rate()
    bot.send_message(message.chat.id, "Курс валют на сегодня:\n USD: " + str(dollar) +"\n EUR: " + str(euro))


def start_contact_notification():
    thread = threading.Thread(target=run_thread)
    thread.start()

def run_thread():
    time_notice_h = 9 # Уведомления статически приходят пользователю в 9 утра 0 минут
    time_notice_m = 0 # 0 минут
    while True:
        current_date = datetime.date.today()        # Узнаем текущую дату
        current_time = datetime.datetime.utcnow()   # Узнаем текущee время сервера по поясу UTC (+00 на сервере)
        for utc in range(-12,12):                   # пробегаемся по всем часовым поясам
            if current_time.hour + utc == time_notice_h and current_time.minute == time_notice_m:  # Уведомление пока настроено статически на 9 утра 0 минут (Но если загрузим на серевер, то он будет будет присылать в 9 утра по времени сервера)
                '''
                Например: Пользователь находится в Москве. Его часовой пояс мы получили при запуске команды /start (Первый запуск бота). Его UTC равен +3
                Время сервера current_time.hour = 6 часов утра
                Время клиента 9 часов утра
                если время сервера + часовой пояс клиента == 9 утра 0 минут, то выполняем дальше
                '''
                db = SQL_Postgre()
                data_contact_withTimeZone = db.get_user_timezone(utc)  # Получаем id-шники тех, у кого часовой пояс utc
                for currData in data_contact_withTimeZone:
                    data_contact = db.find_data_contact(current_date.month, current_date.day, currData[0]) # Получаем данные контактов с указаными id-шниками
                    if len(data_contact) != 0: # Если данные не пустые
                        for row in data_contact:
                            bot.send_message(row[2], 'День рождение у: ' + str(row[0]) + ' ' + str(row[1]) )
                db.close()
        time.sleep(60) # Через минуту запускаем заного


# Запускаем новый поток, который каждый день смотрит кому нужно отправить уведомления из БД контактов
start_contact_notification()



#!------------------------------------------------------------------------------------------!#
# СЕРВЕРНАЯ ЧАСТЬ (НЕ ТРОГАТЬ)
#!------------------------------------------------------------------------------------------!#
"""
@app.route('/' + token, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "POST", 200


@app.route("/")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url='https://miass-bot.herokuapp.com/' + token)
    return "CONNECTED", 200
"""
#app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000)) - это нам не нужно, потому что мы выполняем команду: gunicorn runp-heroku:app

# Если web-хуки не работают или хочешь запустить на локальной машине
# Необходимо закомментировтаь серверную часть и включить bot.polling

#Включить, если не работают веб хуки

#Если появляется ошибка "Conflict: can\'t use getUpdates method while webhook is active", меняем токен бота
# Пишем @botFather
# /revoke
#
# /MiassSuperBot

# или
# heroku ps:scale web=0 #! Отключаем сервер
# Телеграма отработает хуки
# heroku ps:scale web=1 #! Включаем сервер


#или выполняем bot.remove_webhook()
bot.remove_webhook()
bot.polling(none_stop=True)


