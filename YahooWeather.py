__author__ = 'youngsoul'

import string
import feedparser
from YahooGeoPlace import YahooGeoPlace
import re
import platform


class YahooWeather:

    def __init__(self, location=None, degrees='f'):
        self.location = location
        self.results = None
        self.weather_rss_url="http://weather.yahooapis.com/forecastrss?w=$location_woeid&u=$degrees_units"
        self.degrees = degrees  # f or c
        self.subtitle = None
        self.title = None
        self.wind_direction = None
        self.wind_speed = None
        self.wind_chill = None
        self.pressure_units = None
        self.speed_units = None
        self.temperature_units = None
        self.distance_units = None
        self.sunset = None
        self.sunrise = None
        self.pressure = None
        self.pressure_rising = None
        self.visibility = None
        self.humidity = None
        self.conditions_date = None
        self.conditions_temp = None
        self.conditions_text = None
        self.title_detail = None
        self.forecast_summary = None

    def retrieve_weather(self, location=None):
        '''retrieve weather for the given location:
        @param location 'San Francisco CA US'
        '''
        location_to_use = location

        if location_to_use is None:
            location_to_use = self.location

        if location_to_use:
            geo = YahooGeoPlace(location=location_to_use)
            geo.locate()
            woeid = geo.get_woeid()
            url = string.Template(self.weather_rss_url).substitute({"location_woeid":woeid, "degrees_units":self.degrees})
            #print("Weather url: " + url)
            rss = feedparser.parse(url)
            self.results = rss
            print(rss)
            self.title = rss['feed']['title']
            self.subtitle = rss['feed']['subtitle']
            self.pressure_units = rss['feed']['yweather_units']['pressure']
            self.speed_units = rss['feed']['yweather_units']['speed']
            self.temperature_units = rss['feed']['yweather_units']['temperature']
            self.distance_units = rss['feed']['yweather_units']['distance']
            self.sunset = rss['feed']['yweather_astronomy']['sunset']
            self.sunrise = rss['feed']['yweather_astronomy']['sunrise']
            self.pressure = rss['feed']['yweather_atmosphere']['pressure']
            self.pressure_rising = rss['feed']['yweather_atmosphere']['rising']
            self.visibility = rss['feed']['yweather_atmosphere']['visibility']
            self.humidity = rss['feed']['yweather_atmosphere']['humidity']
            self.conditions_date = rss['entries'][0]['yweather_condition']['date']
            self.conditions_temp = rss['entries'][0]['yweather_condition']['temp']
            self.conditions_text = rss['entries'][0]['yweather_condition']['text']
            self.title_detail = rss['entries'][0]['title_detail']['value']

    def generate_summary(self):
        if self.results:
            self.forecast_summary = re.sub('<[^<]+?>', '', self.results['items'][0]['summary_detail']['value'])

            self.forecast_summary = re.sub('Sun -', ' .Sunday. ', self.forecast_summary)
            self.forecast_summary = re.sub('Mon -', ' .Monday. ', self.forecast_summary)
            self.forecast_summary = re.sub('Tue -', ' .Tuesday. ', self.forecast_summary)
            self.forecast_summary = re.sub('Wed -', ' .Wednesday. ', self.forecast_summary)
            self.forecast_summary = re.sub('Thu -', ' .Thursday. ', self.forecast_summary)
            self.forecast_summary = re.sub('Fri -', ' .Friday. ', self.forecast_summary)
            self.forecast_summary = re.sub('Sat -', ' .Saturday ', self.forecast_summary)
            self.forecast_summary = re.sub('Current Conditions:', 'Weather $title_detail. Currently', self.forecast_summary)
            self.forecast_summary = re.sub(' C\n', ' degrees celcius.  \n', self.forecast_summary)
            self.forecast_summary = re.sub(' F\n', ' degrees fahrenheit.  \n', self.forecast_summary)
            self.forecast_summary = re.sub('Forecast:', 'five day Forecast.  \n', self.forecast_summary)
            self.forecast_summary = re.sub('High:', 'High of', self.forecast_summary)
            self.forecast_summary = re.sub('Low:', 'Low of', self.forecast_summary)

            summary = string.Template(self.forecast_summary).substitute({"title_detail":self.title_detail})
            return summary
        else:
            return "No weather data is current available.  "


if __name__ == '__main__':
    y = YahooWeather(location="Cork Ireland", degrees='c')
    y.retrieve_weather()
    weather_summary = y.generate_summary()
    print(weather_summary)
    if platform.system() == 'Linux':
        from GoogleTextToSpeech import GoogleTextToSpeech

        script_dir = "/mnt/ram"
        g = GoogleTextToSpeech(tmp_dir = script_dir)
        g.get_text_to_speech(weather_summary)
        g.play_text_to_speech()
        g.clear()


