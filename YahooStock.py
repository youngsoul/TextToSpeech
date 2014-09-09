__author__ = 'youngsoul'

import string
import urllib
import json
import platform
import re

class YahooStock:

    def __init__(self, symbols=None):
        self.symbols = symbols
        self.results = None
        self.stock_url = "https://query.yahooapis.com/v1/public/yql?q=select * from yahoo.finance.quote where symbol in ('$user_symbols')&format=json&env=store://datatables.org/alltableswithkeys"

    def retrieve_stocks(self, symbols=None):

        symbols_to_use = symbols
        if symbols_to_use is None:
            symbols_to_use = self.symbols

        if symbols_to_use:
            url = string.Template(self.stock_url).substitute({"user_symbols": symbols_to_use})
            #print("url: " + url)
            response = urllib.urlopen(url).read()
            self.results = json.loads(response)
            print(self.results)

    def generate_summary(self):
        summary = "Yahoo stock quotes.  "
        if self.results:
            for quote in self.results['query']['results']['quote'][:self.results['query']['count']]:
                summary += "Stock quote for " + quote['Name'] + " is currently " + quote['Change'] + " changed for the day with a price of " + quote['LastTradePriceOnly'] + ".  "

        summary = re.sub(' Inc.', '.  ', summary)

        return summary


if __name__ == '__main__':
    y = YahooStock(symbols="AAPL,GOOG")
    y.retrieve_stocks()
    stock_summary = y.generate_summary()
    print(stock_summary)
    if platform.system() == 'Linux':
        from GoogleTextToSpeech import GoogleTextToSpeech

        script_dir = "/mnt/ram"
        g = GoogleTextToSpeech(tmp_dir = script_dir)
        g.get_text_to_speech(stock_summary)
        g.play_text_to_speech()
        g.clear()

