from app import app
from app.config import token
from app.db_postgresql import SQL_Postgre
import os
import telebot
from flask import request
import datetime


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
    bot.send_message(message.chat.id, userName + ", Приветствую! Меня зовут " + botName + ". Чем я могу помочь?" )
    list_commands = "Список команд: \n/time - Текущее время\n/contacts - Управление контактами"
    bot.send_message(message.chat.id, list_commands)


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
    db = SQL_Postgre()
    # check_user_availible = True - Пользователь существует в системе
    #                      = False - Пользователь не существует в системе
    check_user_availible = db.check_user_id(userId)
    if check_user_availible == False:
        a = db.new_user(userId,firstName,userName,lastName)
        print(a)
    #query = 'SELECT t.telegram_id FROM public.contact_telegram t  where t.telegram_id = ' + str(userId)
    #a = db.selectAll(query)
    #print(a)
    db.close()

@bot.message_handler(commands=['time'])
def send_time_now(message):
    bot.send_message(message.chat.id, 'Доброе утро, сегодня {dt:%A} {dt:%B} {dt.day}, {dt.year}: '.format(dt = datetime.datetime.now()))

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

