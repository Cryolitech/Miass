from bs4 import BeautifulSoup
from lxml import html
from lxml import etree
import requests

#Функции для получения подробных сведений о погоде на сегодня
def getTodayWeather_full(city):
    url_to_parse = "https://yandex.ru/pogoda/" + city + "/details"
    r = requests.get(url_to_parse)
    response = []
    tree = html.fromstring(r.text)

    #Getting temperature
    morning_temp = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[1]/td[1]/div/div[2]')[0]
    day_temp = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[2]/td[1]/div/div[2]')[0]
    evening_temp = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[3]/td[1]/div/div[2]')[0]
    night_temp = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[4]/td[1]/div/div[2]')[0]

    #Getting description
    morning_desc = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[1]/td[3]')[0]
    day_desc = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[2]/td[3]')[0]
    evening_desc = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[3]/td[3]')[0]
    night_desc = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[4]/td[3]')[0]

    #Getting pressure
    morning_pr = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[1]/td[4]')[0]
    day_pr = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[2]/td[4]')[0]
    evening_pr = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[3]/td[4]')[0]
    night_pr = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[4]/td[4]')[0]

    #Getting humidity
    morning_hum = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[1]/td[5]')[0]
    day_hum = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[2]/td[5]')[0]
    evening_hum = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[3]/td[5]')[0]
    night_hum = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[4]/td[5]')[0]

    #Getting information about the wind
    morning_wind_speed = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[1]/td[6]/div')[0][1]
    day_wind_speed = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[2]/td[6]/div')[0][1]
    evening_wind_speed = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[3]/td[6]/div')[0][1]
    night_wind_speed = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[4]/td[6]/div')[0][1]

    morning_wind_dest = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[1]/td[6]/div')[0][0]
    day_wind_dest = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[2]/td[6]/div')[0][0]
    evening_wind_dest = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[3]/td[6]/div')[0][0]
    night_wind_dest = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[4]/td[6]/div')[0][0]

    morning_wind = morning_wind_speed.text_content() + " " + morning_wind_dest.text_content()
    day_wind = day_wind_speed.text_content() + " " + day_wind_dest.text_content()
    evening_wind = evening_wind_speed.text_content() + " " + evening_wind_dest.text_content()
    night_wind = night_wind_speed.text_content() + " " + night_wind_dest.text_content()

    #Getting "Feels like"-temperature
    morning_feels = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[1]/td[7]/div')[0]
    day_feels = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[2]/td[7]/div')[0]
    evening_feels = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[3]/td[7]/div')[0]
    night_feels = tree.xpath('/html/body/div[3]/div[2]/dd[1]/table/tbody/tr[4]/td[7]/div')[0]

    #response - список
    response.append({
        "Утро": {
            "Температура: ": morning_temp.text_content(),
            "Описание: ": morning_desc.text_content(),
            "Давление": morning_pr.text_content(),
            "Влажность: ": morning_hum.text_content(),
            "Ветер: ": morning_wind,
            "Ощущается как: ": morning_feels.text_content(),
        },
        "День": {
            "Температура: ": day_temp.text_content(),
            "Описание: ":day_desc.text_content(),
            "Давление": day_pr.text_content(),
            "Влажность: ": day_hum.text_content(),
            "Ветер: ": day_wind,
            "Ощущается как: ": day_feels.text_content(),
        },
        "Вечер": {
            "Температура: ": evening_temp.text_content(),
            "Описание: ": evening_desc.text_content(),
            "Давление": evening_pr.text_content(),
            "Влажность: ": evening_hum.text_content(),
            "Ветер: ": evening_wind,
            "Ощущается как: ": evening_feels.text_content(),
        },
        "Ночь": {
            "Температура: ": night_temp.text_content(),
            "Описание: ": night_desc.text_content(),
            "Давление": night_pr.text_content(),
            "Влажность: ": night_hum.text_content(),
            "Ветер: ": night_wind,
            "Ощущается как: ": night_feels.text_content(),
        }
    })

    return response

#Функции для получения подробных сведений о погоде на завтра
def getTommorowWeather_full(city):
    url_to_parse = "https://yandex.ru/pogoda/" + city + "/details"
    r = requests.get(url_to_parse)
    response = []
    tree = html.fromstring(r.text)

    #Getting temperature
    morning_temp = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[1]/td[1]/div/div[2]')[0]
    day_temp = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[2]/td[1]/div/div[2]')[0]
    evening_temp = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[3]/td[1]/div/div[2]')[0]
    night_temp = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[4]/td[1]/div/div[2]')[0]

    #Getting description
    morning_desc = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[1]/td[3]')[0]
    day_desc = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[2]/td[3]')[0]
    evening_desc = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[3]/td[3]')[0]
    night_desc = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[4]/td[3]')[0]

    #Getting pressure
    morning_pr = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[1]/td[4]')[0]
    day_pr = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[2]/td[4]')[0]
    evening_pr = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[3]/td[4]')[0]
    night_pr = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[4]/td[4]')[0]

    #Getting humidity
    morning_hum = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[1]/td[5]')[0]
    day_hum = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[2]/td[5]')[0]
    evening_hum = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[3]/td[5]')[0]
    night_hum = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[4]/td[5]')[0]

    #Getting information about the wind
    morning_wind_speed = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[1]/td[6]/div')[0][1]
    day_wind_speed = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[2]/td[6]/div')[0][1]
    evening_wind_speed = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[3]/td[6]/div')[0][1]
    night_wind_speed = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[4]/td[6]/div')[0][1]

    morning_wind_dest = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[1]/td[6]/div')[0][0]
    day_wind_dest = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[2]/td[6]/div')[0][0]
    evening_wind_dest = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[3]/td[6]/div')[0][0]
    night_wind_dest = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[4]/td[6]/div')[0][0]

    morning_wind = morning_wind_speed.text_content() + " " + morning_wind_dest.text_content()
    day_wind = day_wind_speed.text_content() + " " + day_wind_dest.text_content()
    evening_wind = evening_wind_speed.text_content() + " " + evening_wind_dest.text_content()
    night_wind = night_wind_speed.text_content() + " " + night_wind_dest.text_content()

    #Getting "Feels like"-temperature
    morning_feels = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[1]/td[7]/div')[0]
    day_feels = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[2]/td[7]/div')[0]
    evening_feels = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[3]/td[7]/div')[0]
    night_feels = tree.xpath('/html/body/div[3]/div[2]/dd[3]/table/tbody/tr[4]/td[7]/div')[0]

    #response - список
    response.append({
        "Утро": {
            "Температура: ": morning_temp.text_content(),
            "Описание: ": morning_desc.text_content(),
            "Давление": morning_pr.text_content(),
            "Влажность: ": morning_hum.text_content(),
            "Ветер: ": morning_wind,
            "Ощущается как: ": morning_feels.text_content(),
        },
        "День": {
            "Температура: ": day_temp.text_content(),
            "Описание: ":day_desc.text_content(),
            "Давление": day_pr.text_content(),
            "Влажность: ": day_hum.text_content(),
            "Ветер: ": day_wind,
            "Ощущается как: ": day_feels.text_content(),
        },
        "Вечер": {
            "Температура: ": evening_temp.text_content(),
            "Описание: ": evening_desc.text_content(),
            "Давление": evening_pr.text_content(),
            "Влажность: ": evening_hum.text_content(),
            "Ветер: ": evening_wind,
            "Ощущается как: ": evening_feels.text_content(),
        },
        "Ночь": {
            "Температура: ": night_temp.text_content(),
            "Описание: ": night_desc.text_content(),
            "Давление": night_pr.text_content(),
            "Влажность: ": night_hum.text_content(),
            "Ветер: ": night_wind,
            "Ощущается как: ": night_feels.text_content(),
        }
    })

    return response

#Функции для получения общих сведений о погоде на сегодня
def getTodayWeatherOverall(city):
    url_to_parse = "https://yandex.ru/pogoda/" + city
    r = requests.get(url_to_parse)
    response = []
    tree = html.fromstring(r.text)

    temperature = tree.xpath('/html/body/div[3]/div[1]/div[1]/div[3]/div[1]/a[2]/div')[0]
    precipitation = tree.xpath('/html/body/div[3]/div[1]/div[1]/div[3]/div[1]/div[2]')[0]
    feels_like = tree.xpath('/html/body/div[3]/div[1]/div[1]/div[3]/div[1]/dl[1]/dd')[0]
    wind = tree.xpath('/html/body/div[3]/div[1]/div[1]/div[3]/div[1]/div[3]/dl[1]/dd')[0]
    pressure = tree.xpath('/html/body/div[3]/div[1]/div[1]/div[3]/div[1]/div[3]/dl[2]/dd')[0]
    humidity = tree.xpath('/html/body/div[3]/div[1]/div[1]/div[3]/div[1]/div[3]/dl[3]/dd')[0]

    #response - список
    response.append({
        "Температура: ": temperature.text_content(),
        "Описание: ": precipitation.text_content(),
        "Давление": pressure.text_content(),
        "Влажность: ": humidity.text_content(),
        "Ветер: ": wind.text_content(),
        "Ощущается как: ": feels_like.text_content(),
    })
    return response


#Функция составления финального сообщения для пользователя (string) - для полного отчета
def make_report_full(response):
    report = ''
    for dic in response:
        for key1, value1 in dic.items():
            report = report + key1 + "\n"
            for key2, value2 in value1.items():
                report = report + key2 + "\t" + value2 + "\n"
            report = report + "\n"

    #report - строка
    #print(report)
    return report

#Функция составления финального сообщения для пользователя (string) - для краткого отчета
def make_report_overall(response):
    report = ''
    for dic in response:
        for key, value in dic.items():
            report = report + key + "\t" + value + "\n"
            report = report

    #report - строка
    #print(report)
    return report

#Отладочные функции
'''def main ():
    #getTodayWeather_full('moscow')
    #getTodayWeatherOverall('moscow')
    make_report_full(getTodayWeather_full('moscow'))


if __name__ == "__main__":
    main()'''