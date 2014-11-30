__author__ = 'youngsoul'

import string
import json
import urllib


class YahooHtmlYQL:

    def __init__(self, html_url=None, xpath=None):
        self.results = None
        self.html_url = html_url
        self.xpath = xpath
        self.yql_url = "https://query.yahooapis.com/v1/public/yql?format=json&q=select * from html where url=\"$html_url\" and xpath=\"$xpath\""

    def retrieve_html(self, html_url=None, xpath=None):
        html_url_to_use = html_url
        xpath_to_use = xpath

        if html_url_to_use is None:
            html_url_to_use = self.html_url

        if xpath_to_use is None:
            xpath_to_use = self.xpath

        html_url_to_use = urllib.quote_plus(html_url_to_use)
        xpath_to_use = urllib.quote_plus(xpath_to_use)

        if html_url_to_use and xpath_to_use:
            url = string.Template(self.yql_url).substitute({"html_url": html_url_to_use,
                                                            "xpath": xpath_to_use})
            print("url: " + url)
            response = urllib.urlopen(url).read()
            self.results = json.loads(response)

    def generate_summary(self):
        print("results: " + str(self.results))

if __name__ == '__main__':
    '''
    install xpath helper in chrome
    https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl?hl=en
    '''

    url = "http://www.timeanddate.com/countdown/to?iso=20161108T07&p0=611&msg=Countdown+until+Obama+is+OUT+OF+OFFICE"
    day_xpath = "/html/body[@class='tpl-generic']/div[@class='main-content-div']/div[@class='fixed']/div[@id='cnt_main']/div[@class='cnt-main']/p[@id='rs2']/span[@id='el_d1']"

    hour_xpath = "/html/body[@class='tpl-generic']/div[@class='main-content-div']/div[@class='fixed']/div[@id='cnt_main']/div[@class='cnt-main']/p[@id='rs2']/span[@id='el_h1']"

    min_xpath = "/html/body[@class='tpl-generic']/div[@class='main-content-div']/div[@class='fixed']/div[@id='cnt_main']/div[@class='cnt-main']/p[@id='rs2']/span[@id='el_m1']"

    y = YahooHtmlYQL()
    y.retrieve_html(url, day_xpath)
    y.generate_summary()

    y.retrieve_html(url, hour_xpath)
    y.generate_summary()

    y.retrieve_html(url, min_xpath)
    y.generate_summary()
