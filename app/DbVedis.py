# -*- coding: utf-8 -*-

from vedis import Vedis
import app.config as config

# Пытаемся узнать из базы «состояние» пользователя
# Состояния описаны в файле config в классе - class States(Enum)
#
def get_current_state(user_id):
    with Vedis(config.db_status) as db:
        try:
            return db[user_id]
        except KeyError:  # Если такого ключа почему-то не оказалось
            return config.States.S_START.value  # значение по умолчанию - начало диалога

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id,state):
    with Vedis(config.db_status) as db:
        try:
            db[user_id] = state
            return True
        except KeyError:
            return False


def get_current_hash(user_id,key):
    with Vedis(config.db_status) as db:
        h = db.Hash(str(user_id))
        try:
            return h.to_dict()
        except KeyError:  # Если такого ключа почему-то не оказалось
            return 0  # значение по умолчанию - начало диалога

def set_hash_timezone(user_id, value):
    with Vedis(config.db_status) as db:
        h = db.Hash(str(user_id))
        try:
            h['timezone'] = value
            return True
        except:
            # тут желательно как-то обработать ситуацию
            return False

def getData_from_id(user_id):
    with Vedis(config.db_status) as db:
        h = db.Hash(str(user_id))
        try:
            data = {}
            data['user_id'] = user_id
            data['timezone'] = h['timezone']
            data['city'] = h['city']
            data['time_notice_status'] = h['time_notice_status']
            data['currency_notice_status'] = h['currency_notice_status']
            data['weather_notice_status'] = h['weather_notice_status']
            return data
        except:
            return 0
def setUserData(user_id,timezone,city,time_notice_status,currency_notice_status,weather_notice_status):
    with Vedis(config.db_status) as db:
        h = db.Hash(str(user_id))
        try:
            if time_notice_status == True:
                time_notice_status = '1'
            else:
                time_notice_status = '0'

            if currency_notice_status == True:
                currency_notice_status = '1'
            else:
                currency_notice_status = '0'

            if weather_notice_status == True:
                weather_notice_status = '1'
            else:
                weather_notice_status = '0'

            h['timezone'] = str(timezone)
            h['city'] = str(city)
            h['time_notice_status'] = time_notice_status
            h['currency_notice_status'] = currency_notice_status
            h['weather_notice_status'] = weather_notice_status
            return True
        except:
            return False

def set_hash_city(user_id, value):
    with Vedis(config.db_status) as db:
        h = db.Hash(str(user_id))
        try:
            city = value.title()
            h['city'] = city
            return True
        except:
            # тут желательно как-то обработать ситуацию
            return False
def get_hash_timezone(user_id):
    with Vedis(config.db_status) as db:
        h = db.Hash(str(user_id))
        try:
            return h['timezone']
        except:
            # тут желательно как-то обработать ситуацию
            return "error"

def update_hash_notice(user_id,new_notice,status):
    with Vedis(config.db_status) as db:
        h = db.Hash(str(user_id))
        try:
            h[new_notice] = status
        except:
            h[new_notice] = "0" #Статус не активен
def get_hash_city(user_id):
    with Vedis(config.db_status) as db:
        h = db.Hash(str(user_id))
        try:
            return h['city']
        except:
            # тут желательно как-то обработать ситуацию
            return "error"
def get_current_position(user_id):
    with Vedis(config.db_position) as db:
        try:
            return db[user_id]
        except KeyError:  # Если такого ключа почему-то не оказалось
            return config.Position.S_START.value  # значение по умолчанию - начало диалога

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_position(user_id, value):
    with Vedis(config.db_position) as db:
        try:
            db[user_id] = value
            return True
        except:
            # тут желательно как-то обработать ситуацию
            return False

