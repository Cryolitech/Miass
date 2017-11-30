from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from xml.etree import ElementTree as ET


def current_exchange_rate():
    """Получает значения доллара и евро в рублях на время запуска. Данные берутся с сайта ЦБР. Возвращает значение доллара в рублях, евро в рублях"""
    rub_dollar = ''
    rub_evro = ''
    try:
        ratesFile = urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req")
    except HTTPError as e:
        print('Error code: ', e.code)
    except URLError as e:
        print('Error code: ', e.reason)
    else:
        id_dollar = "R01235" # Константные переменные
        id_evro = "R01239"

        valuta = ET.parse(ratesFile)

        for line in valuta.findall('Valute'):
            id_v = line.get('ID')
            if id_v == id_dollar:
                rub_dollar = line.find('Value').text
            if id_v == id_evro:
                rub_evro = line.find('Value').text
        return [rub_dollar,rub_evro]
