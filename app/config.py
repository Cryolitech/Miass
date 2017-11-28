# -*- coding: utf-8 -*-
from enum import Enum

# Токен бота
token = '431904557:AAHpjz8Qtnekh-lNsj8q7SG3IFvFSq_yuZ0'

#PostgerSQL
Database_name = "dam200ta40ispa"
Username = "tvqpoqthrrskcc"
Password = "bf52ed097dcffbb71d9fb127149f9e1e9b97c16178cc1837a5ac8ccf0ce5e100"
Hostname = "ec2-54-225-88-191.compute-1.amazonaws.com"
Port = "5432"

# БД Vedis для хранения статуса пользователя при настройках
db_status = "status.vdb"
db_position = "curr_pos.vdb"
class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"           # Начало нового диалога
    S_ENTER_TIMEZONE = "1"  # На этапе выбора часового пояса
    S_ENTER_CITY = "2"      # На этапе выбора города
    S_CHECKINOK = "3"       # Зарегестрированный статус. Есть доступ к почти всем функциям бота.
                            # Почему почти?
                            # Например файл, где хранятся контакты и данные из социальных сетей не обязательны.
                            # Их пользователь вводит потом, при необходимости.

class Position(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"                       # Инициализация
    S_CONTACTS = "1"                    # Пользователь нажал /contacts
    S_CREATE_CONTACTS_FILE = "2"        # Пользователь нажал /createContact
