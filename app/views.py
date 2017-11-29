# -*- coding: utf-8 -*-
from app import app
from app.config import token #Забираем токен из config.py (Этот файл содержит переменную token c занчением, выдаваемым botfather в telegram)
import app.config as config
from app.db_postgresql import SQL_Postgre
from app.csvEditor import csv_dict_reader
from app.ExchangeRates import current_exchange_rate
from telebot import types
import os
import re
import telebot
from flask import request
from app.timezone import get_utc_offset_timezone, get_time_from_another_timezone
import requests
import datetime
import time
import threading
import shelve
from app.DbVedis import get_current_state,set_state,set_hash_city,set_hash_timezone,get_current_hash,get_hash_timezone, set_position, get_current_position,get_hash_city,getData_from_id,update_hash_notice,setUserData
import app.weather as weather

import _thread

bot = telebot.TeleBot(token)
def inRange(num, min, max):
    if num in range(min,max):
        return True
    else:
        return False



@bot.message_handler(commands=['start'])
def send_welcome(message):
    userId = message.from_user.id  # id пользователя в telegram
    firstName = message.from_user.first_name  # Имя пользователя
    userName = message.from_user.username  # Имя, отображающееся в telegram
    lastName = message.from_user.last_name  # Фамилия пользователя

    botName = bot.get_me().first_name  # Берем имя бота
    bot.send_message(message.chat.id, str(userName) + ", Приветствую! Меня зовут " + str(botName) + ". Чем я могу тебе помочь?")
    db = SQL_Postgre()
    if db.check_user_id(message.chat.id) == False:
        db.new_user(userId, firstName, userName, lastName)
    db.close()

    curr_state = get_current_state(message.chat.id)
    if curr_state == config.States.S_CHECKINOK.value:
        pass
    if curr_state == config.States.S_START.value: # Первый вход
        bot.send_message(message.chat.id, "Похоже, вы у нас в первый раз. Ну ничего страшного, для начала мне понадобятся некоторые данные." )
        set_state(message.chat.id, config.States.S_ENTER_TIMEZONE.value)
        setUTC(message)
        return
    elif curr_state == config.States.S_ENTER_TIMEZONE.value:
        setUTC(message)
        return
    elif curr_state == config.States.S_ENTER_CITY.value:
        set_city(message)
        bot.send_message(message.chat.id,
                         userName + "Чтобы общаться со мной, введите команду /Miass")
        # После ввода последней настройки вызываем для иництализации
        get_current_position(message.chat.id)
        return
        # После регистрации клиента в системе выводим первое приветсвие
    bot.send_message(message.chat.id, "/Miass - твоя персональная помощница\n"
                                      "/settings - мои настройки\n"
                                      "/reset_settings - сбросить настройки ")


    """
   
    # Получаем данные
    userId = message.from_user.id # id пользователя в telegram
    # Являетеся ли ботом? В документации есть is_bot
    firstName = message.from_user.first_name # Имя пользователя
    userName = message.from_user.username # Имя, отображающееся в telegram
    lastName = message.from_user.last_name # Фамилия пользователя
    languageCode = message.from_user.language_code # Используемый язык
    #msg_date = message.date #Дата отправки /start

    db = SQL_Postgre()
    # check_user_availible = True - Пользователь существует в системе
    #                      = False - Пользователь не существует в системе
    check_user_availible = db.check_user_id(userId)
    if check_user_availible == False:

        # После регистрации клиента в системе выводим первое приветсвие
        
        bot.send_message(message.chat.id, userName + ", Приветствую! Меня зовут " + botName + ". Я могу помочь вам в решении повседневных задач. Чтобы я смогла вас зарегестрировать в системе, пожалуйста, ответьте на вопросы")
        bot.send_message(message.chat.id, 'Введите ваш часовой пояс (от -12 до +12): \nНапример: +3')


        curr_utc_time = datetime.datetime.utcnow()
        timezone = get_utc_offset_timezone(curr_utc_time, msg_date)
        a = db.new_user(userId, firstName, userName, lastName, timezone)
    else:
        bot.send_message(message.chat.id, userName + ", Приветствую! Меня зовут " + botName + ". Чем я могу помочь?")
        list_subscriptions = "/currentSubscriptions - текущие подписки"
        bot.send_message(message.chat.id, list_subscriptions)
        list_commands = "Список команд: \n/time - Текущее время\n/contacts - Управление контактами\n/currency - курс валют"
        bot.send_message(message.chat.id, list_commands)

    db.close()
    """

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_ENTER_TIMEZONE.value)
def set_timezone(message):
    msg = message.text
    if msg.isdigit():
        if inRange(int(msg),-11,12):
            bot.send_message(message.chat.id, "Теперь укажите ближайший город.")
            set_hash_timezone(message.chat.id,msg)
            set_state(message.chat.id, config.States.S_ENTER_CITY.value)
        else:
            bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!")
    else:
        bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!")

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == config.States.S_ENTER_CITY.value)
def set_city(message):
    msg = message.text
    # !!! Тут нужно сделать проверку город с помощью регулярного выражения!!!
    list_city = ['Москва','москва','Moscow','moscow']
    if str(msg) in list_city:
        check = True
    else:
        check = False

    #db = SQL_Postgre()
    #check = db.check_city(str(msg))
    #db.close()
    if check == True:
        bot.send_message(message.chat.id, "Отлично! Я к твоим услугам. Чтобы общаться со мной, введи команду /Miass")
        db = SQL_Postgre()

        set_hash_city(message.chat.id,'Moscow')
        utc = get_hash_timezone(message.chat.id)

        db.update_user(message.chat.id, utc, 'Moscow')
        db.close()
        set_state(message.chat.id, config.States.S_CHECKINOK.value) # Теперь переводим в статус зарегестрированного
    else:
        bot.send_message(message.chat.id, "Похоже твоего города нет в списке. Введи Москва (Я пока в бета-версии) :)")
        #bot.send_message(message.chat.id, "Похоже твоего города нет в списке. Но не переживай, я это скоро исправлю. А пока введите ближайший к вашему городу. ")

@bot.message_handler(commands=['commands'])
def view_commands(message):
    bot.send_message(message.chat.id, "Список команд:\n"
                                      "/time - текущее время\n"
                                      "/currency - курс валют на сегодня\n"
                                      "/weather - погода на сегодня\n"
                                      "/weatherFull - подробный прогноз погоды  на сегодня\n"
                                      #"/contacts - управление контактами"
                                      )

@bot.message_handler(commands=['UpdateVedis'])
def update_vedis(message):
    db = SQL_Postgre()
    lst = db.getAllUserInfo()
    for i in lst:
        setUserData(i[0], i[4], i[5], i[6], i[7], i[8])
    db.close()
    

@bot.message_handler(commands=['Miass'])
def view_miass_commands(message):
    bot.send_message(message.chat.id, "Чем я могу тебе помочь?\n"
                                      "/services - мои сервисы. Нажмите, чтобы посмотреть весь список\n"
                                      "/settings - настройки\n"
                                      "/commands - список команд" )
    view_commands(message)

@bot.message_handler(commands=['services'])
def view_miass_commands(message):
    bot.send_message(message.chat.id, "Выбери сервис, который тебя интересует. Каждые 9 утра я буду присылать уведомления.\n"
                                      "/activateTime - дата и время \n"
                                      "/activateCurrency - курс валют\n"
                                      "/activateWeather - погода\n"
                                      "/activatedServices - мои текущие подписки\n"
                                      "/disableServices - открючить сервис" )

@bot.message_handler(commands=['disableServices'])
def disable_services(message):
    bot.send_message(message.chat.id, "Выбери сервис, который хочешь отключить.\n"
                                      "/disableAll - отключить все сервисы\n"
                                      "/disableTime - открючить уведомление даты и время\n"
                                      "/disableCurrency - отключить уведомление курса валют\n"
                                      "/disableWeather - отключить уведомление погоды" )

@bot.message_handler(commands=['activatedServices'])
def view_activated_services(message):
    data = getData_from_id(message.chat.id)

    if data['time_notice_status'] != '0':
        time = 'Уведомление даты и времени включено'
    else:
        time = 'Уведомление даты и времени отключено'

    if data['currency_notice_status'] != '0':
        currency = 'Уведомление курса валют включено'
    else:
        currency = 'Уведомление курса валют отключено'

    if data['weather_notice_status'] != '0':
        weather = 'Уведомление погоды включено'
    else:
        weather = 'Уведомление погоды отключено'

    text = 'Подписки: \n' + time + "\n" + currency + "\n" + weather
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['activateTime'])
def activate_time_notice(message):
    update_hash_notice(message.chat.id, 'time_notice_status','1')
    bot.send_message(message.chat.id,'Подписка оформлена')
    db = SQL_Postgre()
    db.update_time_notice_status(message.chat.id, True)
    db.close()

@bot.message_handler(commands=['activateCurrency'])
def activate_currency_notice(message):
    update_hash_notice(message.chat.id, 'currency_notice_status', '1')
    bot.send_message(message.chat.id, 'Подписка оформлена')
    db = SQL_Postgre()
    db.update_currency_notice_status(message.chat.id, True)
    db.close()
@bot.message_handler(commands=['activateWeather'])
def activate_weather_notice(message):
    update_hash_notice(message.chat.id, 'weather_notice_status', '1')
    bot.send_message(message.chat.id, 'Подписка оформлена')
    db = SQL_Postgre()
    db.update_weather_notice_status(message.chat.id, True)
    db.close()

@bot.message_handler(commands=['disableAll'])
def disactivate_notice_all(message):
    update_hash_notice(message.chat.id, 'time_notice_status','0')
    update_hash_notice(message.chat.id, 'currency_notice_status', '0')
    update_hash_notice(message.chat.id, 'weather_notice_status', '0')
    bot.send_message(message.chat.id, 'Отписка от всех уведомлений. Почему? Надеюсь, это в последний раз :(')
    db = SQL_Postgre()
    db.update_user_notice(message.chat.id, False,False,False)
    db.close()
@bot.message_handler(commands=['disableTime'])
def disactivate_time_notice(message):
    update_hash_notice(message.chat.id, 'time_notice_status','0')
    bot.send_message(message.chat.id, 'Отписка от уведомления')
    db = SQL_Postgre()
    db.update_time_notice_status(message.chat.id, False)
    db.close()

@bot.message_handler(commands=['disableCurrency'])
def disactivate_currency_notice(message):
    update_hash_notice(message.chat.id, 'currency_notice_status', '0')
    bot.send_message(message.chat.id, 'Отписка от уведомления')
    db = SQL_Postgre()
    db.update_currency_notice_status(message.chat.id, False)
    db.close()
@bot.message_handler(commands=['disableWeather'])
def disactivate_weather_notice(message):
    update_hash_notice(message.chat.id, 'weather_notice_status', '0')
    bot.send_message(message.chat.id, 'Отписка от уведомления')
    db = SQL_Postgre()
    db.update_weather_notice_status(message.chat.id, False)
    db.close()
@bot.message_handler(commands=['settings'])
def user_settings(message):
    bot.send_message(message.chat.id, "Ваш часовой пояс: " + str(get_hash_timezone(message.chat.id)) + "\nВаш город:                " + str(get_hash_city(message.chat.id)) + "\nСброс настроек: /resetSettings" )

@bot.message_handler(commands=['resetSettings'])
def reset_settings(message):
    bot.send_message(message.chat.id, "Сбрасываю настройки.")
    set_state(message.chat.id, config.States.S_ENTER_TIMEZONE.value)
    setUTC(message)

@bot.message_handler(commands=["setUTC"])
def setUTC(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    UTCminus11 = types.KeyboardButton('-11')
    UTCminus10 = types.KeyboardButton('-10')
    UTCminus9 = types.KeyboardButton('-9')
    UTCminus8 = types.KeyboardButton('-8')
    UTCminus7 = types.KeyboardButton('-7')
    UTCminus6 = types.KeyboardButton('-6')
    UTCminus5 = types.KeyboardButton('-5')
    UTCminus4 = types.KeyboardButton('-4')
    UTCminus3 = types.KeyboardButton('-3')
    UTCminus2 = types.KeyboardButton('-2')
    UTCminus1 = types.KeyboardButton('-1')
    UTCZero = types.KeyboardButton('0')
    UTC1 = types.KeyboardButton('1')
    UTC2 = types.KeyboardButton('2')
    UTC3 = types.KeyboardButton('3')
    UTC4 = types.KeyboardButton('4')
    UTC5 = types.KeyboardButton('5')
    UTC6 = types.KeyboardButton('6')
    UTC7 = types.KeyboardButton('7')
    UTC8 = types.KeyboardButton('8')
    UTC9 = types.KeyboardButton('9')
    UTC10 = types.KeyboardButton('10')
    UTC11 = types.KeyboardButton('11')
    UTC12 = types.KeyboardButton('12')
    markup.row(UTCminus11, UTCminus10, UTCminus9, UTCminus8, UTCminus7, UTCminus6, UTCminus5, UTCminus4, UTCminus3,
               UTCminus2, UTCminus1, UTCZero)
    markup.row(UTC1, UTC2, UTC3, UTC4, UTC5, UTC6, UTC7, UTC8, UTC9, UTC10, UTC11, UTC12)
    bot.send_message(message.chat.id, "Пожалуйста, введите часовой пояс:", reply_markup=markup)


@bot.message_handler(commands=["geophone"])
def geophone(message):
    # Эти параметры для клавиатуры необязательны, просто для удобства
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_phone, button_geo)
    bot.send_message(message.chat.id, "Отправь мне свой номер телефона или поделись местоположением, жалкий человечишка!", reply_markup=keyboard)

@bot.message_handler(commands=['time'])
def send_time_now(message):
    user_timezone = get_hash_timezone(message.chat.id)
    if user_timezone != "error":
        currDTime = datetime.datetime.fromtimestamp(message.date)
        curr_user_time = get_time_from_another_timezone(currDTime,int(user_timezone))
        bot.send_message(message.chat.id, 'Сегодня {:%d %b %Y, %H:%M } '.format(curr_user_time))
    else:
        set_state(message.chat.id, "1")
        bot.send_message(message.chat.id, 'Не указан часовой пояс. Пройдите регистрацию /start')

@bot.message_handler(commands=['contacts'])
def send_welcome_contacts(message):
    bot.send_message(message.chat.id, "Список команд:\n /createContact - Загрузить контакты файлом")
    set_position(message.chat.id, config.Position.S_CONTACTS.value)

@bot.message_handler(commands=['createContact'],func=lambda message: get_current_position(message.chat.id) == config.Position.S_CONTACTS.value)
def new_contact_list(message):
    bot.send_message(message.chat.id, 'Пожалуйста, загрузите файл в формате GOOGLE CSV\nПодробнее: https://www.google.com/contacts/u/0/?cplus=0#contacts\nЕще->Экспорт->Выберите формат файла для экспорта->\nGoogle CSV (для импорта в аккаунт Google)')
    set_position(message.chat.id, config.Position.S_CREATE_CONTACTS_FILE.value)

# Загрузка документа
@bot.message_handler(content_types=['document'],func=lambda message: get_current_position(message.chat.id) == config.Position.S_CREATE_CONTACTS_FILE.value)
def downloadFile(message):
    userId = message.from_user.id
    a = message.document.file_id
    file_info = bot.get_file(a)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    csv_dict_reader(file.text, userId)
    bot.send_message(message.chat.id, "Файл успешно загружен.")
    set_position(message.chat.id, config.Position.S_START.value)

@bot.message_handler(content_types=['document'])
def allDocs(message):
    bot.send_message(message.chat.id, "И что это? Я не знаю зачем мне твой файл")

@bot.message_handler(commands=['currency'])
def send_exchange_rates(message):
    dollar,euro = current_exchange_rate()
    bot.send_message(message.chat.id, "Курс валют на сегодня:\nUSD: " + str(dollar) +"\nEUR: " + str(euro))

@bot.message_handler(commands=['weatherFull'])
def send_exchange_rates(message):
    city = get_hash_city(message.chat.id) # Берем город по id пользователя
    if city != "error":
        curr_weather = weather.make_report_full(weather.getTodayWeather_full(str(city)))
        bot.send_message(message.chat.id, "Погода на сегодня:\n" + str(curr_weather))
    else:
        set_state(message.chat.id, "2") # Перевод пользователя в статус 2 - необходимо указать город
        bot.send_message(message.chat.id, 'Не указан город. Пройдите регистрацию /start')

@bot.message_handler(commands=['weather'])
def send_exchange_rates(message):
    city = get_hash_city(message.chat.id) # Берем город по id пользователя
    if city != "error":
        curr_weather = weather.make_report_overall(weather. getTodayWeatherOverall(str(city)))
        bot.send_message(message.chat.id, "Погода на сегодня:\n" + str(curr_weather))
    else:
        set_state(message.chat.id, "2") # Перевод пользователя в статус 2 - необходимо указать город
        bot.send_message(message.chat.id, 'Не указан город. Пройдите регистрацию /start')




def foo(x, s):
    print("%s %s %s" % (threading.current_thread(), x, s))
    while True:
        id = 61714776  # row['user_id']
        bot.send_message(id, "hello")
        time.sleep(s)  # Через минуту запускаем заного


for x in range(1):
    threading.Thread(target=foo, args=(x, 60)).start()



#!------------------------------------------------------------------------------------------!#
# СЕРВЕРНАЯ ЧАСТЬ (НЕ ТРОГАТЬ)
#!------------------------------------------------------------------------------------------!#

@app.route('/' + token, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "POST", 200


@app.route("/")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url='https://protected-plateau-16454.herokuapp.com/'+ token)
    return "CONNECTED", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))

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

"""
bot.remove_webhook()
bot.polling(none_stop=True)
"""

