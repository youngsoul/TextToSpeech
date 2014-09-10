__author__ = 'youngsoul'

import string
import urllib
import json


class YahooGeoPlace:

    def __init__(self, location=None):
        self.location = location
        self.results = None
        self.geo_place_url="http://query.yahooapis.com/v1/public/yql?format=json&q=select * from geo.places where text='$user_location'"

    def locate(self, location=None):
        # see if user wants to overide the location from the init method
        location_to_use = location
        if not location_to_use:
            location_to_use = self.location

        if location_to_use:
            url = string.Template(self.geo_place_url).substitute({"user_location": location_to_use})
            #print("GeoPlaceUrl: " + url)
            #query.results.place.woeid
            response = urllib.urlopen(url).read()
            self.results = json.loads(response)
            #print(self.results['query']['results']['place']['woeid'])

    def get_woeid(self):
        if self.results:
            if type(self.results['query']['results']['place']) is dict:
                return self.results['query']['results']['place']['woeid']
            else:
                return self.results['query']['results']['place'][0]['woeid']
        else:
            return None


if __name__ == '__main__':
    y = YahooGeoPlace(location="Boston MA US")
    y.locate()
    print("Results: " + y.get_woeid())

