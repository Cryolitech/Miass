import os
from urllib import parse
import psycopg2
import sys

class SQL_Postgre:
    def __init__(self):
        # ! параметры БД
        self.database_name = "dam200ta40ispa"
        self.username = "tvqpoqthrrskcc"
        self.password = "bf52ed097dcffbb71d9fb127149f9e1e9b97c16178cc1837a5ac8ccf0ce5e100"
        self.hostname = "ec2-54-225-88-191.compute-1.amazonaws.com"
        self.port = "5432"
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
            query = 'SELECT t.telegram_id FROM public.contact_telegram t  where t.telegram_id = ' + str(telegramId)
            cur.execute(query)
            data = cur.fetchone()
            cur.close()
            if data != None:
                return True     # Пользователь есть в БД
            else:
                return False    # Пользователья нет в БД

    def new_user(self, userId,firstName,userName,lastName,timezone):
        cur = self.conn.cursor()
        self.cur.execute("insert into contact_telegram(telegram_id,first_Name,user_Name,last_Name,timezone) values(%s,%s,%s,%s,%s)",(str(userId),str(firstName),str(userName),str(lastName),str(timezone)))
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
            query = 'SELECT DISTINCT telegram_id,timezone FROM public.contact_telegram WHERE timezone = ' + str(timezone)
            cur.execute(query)
            data = cur.fetchall()
            cur.close()
            return data

    def close(self):
        self.cur.close()    # Закрываем курсор
        self.conn.close()   # Закрываем соеднинение с БД

