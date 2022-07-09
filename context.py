import requests, json
from datetime import datetime
import pytz
import re

api_key = '' # put you API key

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

city = 'Rouen'

complete_url = BASE_URL  + "appid=" + api_key + "&q=" + city


class Weather:
    def __init__(self, url):
        self.url = url
    
    def take_weather(self):

        response = requests.get(self.url)
        if response.status_code == 200:
        # getting data in the json format
            data = response.json()
            # getting the main dict block
            report = data['weather']
            return report[0]['description']
        else:
            # showing the error message
            print("Error in the HTTP request")
    
    def get_weather(self):
        weather_type = self.take_weather()
        if re.search('rain', weather_type):
            return 'rainy'
        else: 
            return weather_type


class Time:
    def __init__(self):
        pass

    def get_time(self):
        tz_Rouen = pytz.timezone('Europe/Paris') 
        datetime_Rouen = datetime.now(tz_Rouen)
        time = datetime_Rouen.strftime("%H:%M")
        if ('07:00' <= time < '12:00') or ('14:00' <= time < '18:00'):
            return 'daytime'
        elif '12:00' <= time < '14:00':
            return 'lunchtime'
        else:
            return 'nighttime'


Rouen_w = Weather(complete_url)
current_weather = Rouen_w.get_weather()


Rouen_t = Time()
current_time = Rouen_t.get_time()
