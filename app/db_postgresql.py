import os
from urllib import parse
import psycopg2
import sys
import app.config as config

class SQL_Postgre:
    def __init__(self):
        # ! параметры БД
        self.database_name = config.Database_name
        self.username = config.Username
        self.password = config.Password
        self.hostname = config.Hostname
        self.port = config.Port
        # !

        self.conn = psycopg2.connect(
            database=self.database_name,
            user=self.username,
            password=self.password,
            host=self.hostname,
            port=self.port
        )
        self.cur = self.conn.cursor()

    def check_user_id(self, telegramId):
        with self.conn:
            cur = self.conn.cursor()
            query = 'SELECT DISTINCT t.telegram_id FROM public.contact_telegram t  where t.telegram_id = ' + str(telegramId)
            cur.execute(query)
            data = cur.fetchone()
            cur.close()
            if data != None:
                return True     # Пользователь есть в БД
            else:
                return False    # Пользователья нет в БД
    def getAll_user_id(self):
        with self.conn:
            cur = self.conn.cursor()
            query = 'SELECT telegram_id FROM public.contact_telegram'
            cur.execute(query)
            data = cur.fetchall()
            cur.close()
            if data != None:
                return list(data)     # Пользователь есть в БД
            else:
                return None    # Пользователья нет в БД

    def getAllUserInfo(self):
        with self.conn:
            cur = self.conn.cursor()
            query = 'SELECT * FROM public.contact_telegram'
            cur.execute(query)
            data = cur.fetchall()
            cur.close()
            if data != None:
                return list(data)     # Пользователь есть в БД
            else:
                return None    # Пользователья нет в БД
    def check_city(self, city_name):
        with self.conn:
            cur = self.conn.cursor()
            city = city_name.title()
            query = 'SELECT name FROM city WHERE name = ' +str("'" + city + "'")
            #cur.execute("SELECT name FROM city WHERE name = '"+city_name+"'")
            cur.execute(query)
            data = cur.fetchone()
            cur.close()
            if data != None:
                return True     # Город есть в БД
            else:
                return False    # Города нет в БД

    def new_user(self, userId,firstName,userName,lastName):
        cur = self.conn.cursor()
        self.cur.execute("insert into contact_telegram(telegram_id,first_Name,user_Name,last_Name) values(%s,%s,%s,%s)",(str(userId),str(firstName),str(userName),str(lastName)))
        self.conn.commit()  # Загружае все звпросы на сервер БД
        cur.close()
        return True
    def update_user(self, userId,timezone,city):
        cur = self.conn.cursor()
        query = 'UPDATE contact_telegram SET  timezone = ' + str(timezone) + ', city = ' + str("'" + city + "'") + ' WHERE telegram_id =' + str(userId)
        self.cur.execute(query)
        self.conn.commit()  # Загружае все звпросы на сервер БД
        cur.close()
        return True

    def update_user_notice(self,userId, time_notice_status,currency_notice_status,weather_notice_status):
        cur = self.conn.cursor()
        query = 'UPDATE contact_telegram SET  time_notice_status = ' + str(time_notice_status) + ', currency_notice_status = ' + str(currency_notice_status) + ', weather_notice_status = ' + str(weather_notice_status) + ' WHERE telegram_id = ' + str(userId)
        self.cur.execute(query)
        self.conn.commit()  # Загружае все звпросы на сервер БД
        cur.close()
        return True
    def update_time_notice_status(self,userId, time_notice_status):
        cur = self.conn.cursor()
        query = 'UPDATE contact_telegram SET  time_notice_status = ' + str(time_notice_status) + ' WHERE telegram_id = ' + str(userId)
        self.cur.execute(query)
        self.conn.commit()  # Загружае все звпросы на сервер БД
        cur.close()
        return True
    def update_currency_notice_status(self,userId, currency_notice_status):
        cur = self.conn.cursor()
        query = 'UPDATE contact_telegram SET  currency_notice_status = ' + str(currency_notice_status) + ' WHERE telegram_id = ' + str(userId)
        self.cur.execute(query)
        self.conn.commit()  # Загружае все звпросы на сервер БД
        cur.close()
        return True

    def update_weather_notice_status(self, userId, weather_notice_status):
        cur = self.conn.cursor()
        query = 'UPDATE contact_telegram SET  weather_notice_status = ' + str(weather_notice_status) + ' WHERE telegram_id = ' + str(userId)
        self.cur.execute(query)
        self.conn.commit()  # Загружае все звпросы на сервер БД
        cur.close()
        return True

    def selectAll(self,query):
        with self.conn:
            self.cur.execute(query)
            results = self.cur.fetchall()
            return results

    def new_contacts(self,name, birth, user_id):
        with self.conn:
            cur = self.conn.cursor()
            self.cur.execute("insert into contact_users(name, birth,contact_user_id) values(%s,%s,%s)",(str(name),str(birth),str(user_id)))
            self.conn.commit()  # Загружае все звпросы на сервер БД
            cur.close()
            return True

    def check_contacts(self,telegramId):
        with self.conn:
            query = 'SELECT DISTINCT contact_user_id FROM public.contact_users WHERE contact_user_id = 61714776;'
            self.cur.execute(query)
            if self.cur.fetchone() == None:
                return False
            else:
                return True

    def delete_contacts(self,telegramId):
        with self.conn:
            self.cur.execute("DELETE FROM contact_users WHERE contact_user_id = " + str(telegramId))
            self.conn.commit()  # Загружае все звпросы на сервер БД

    def find_data_contact(self,month,day,contact_user_id):
        with self.conn:
            cur = self.conn.cursor()
            query = 'SELECT  name,birth,contact_user_id FROM public.contact_users WHERE Extract(month from birth) = ' + str(month) + ' AND Extract(day from birth) = ' + str(day) + ' and contact_user_id = ' + str(contact_user_id)
            cur.execute(query)
            data = cur.fetchall()
            cur.close()
            return data
    def get_user_timezone(self,timezone):
        with self.conn:
            cur = self.conn.cursor()
            query = 'SELECT telegram_id,timezone FROM public.contact_telegram WHERE timezone = ' + str(timezone)
            cur.execute(query)
            data = cur.fetchall()
            cur.close()
            return data
    def get_timezone_fromId(self,user_id):
        with self.conn:
            cur = self.conn.cursor()
            query = 'SELECT timezone FROM public.contact_telegram WHERE telegram_id = ' + str(user_id)
            cur.execute(query)
            data = cur.fetchone()
            cur.close()
            return data

    def close(self):
        self.cur.close()    # Закрываем курсор
        self.conn.close()   # Закрываем соеднинение с БД

