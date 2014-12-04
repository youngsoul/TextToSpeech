__author__ = 'youngsoul'

import string
import urllib
import json
import platform
import random


class YahooRss:

    def __init__(self, rss_url=None, max_stories=7):
        self.rss_url = rss_url
        self.yql_rss_url = "https://query.yahooapis.com/v1/public/yql?format=json&q=SELECT title,entry.title,entry.summary.content FROM feednormalizer WHERE output='atom_1.0' AND url='$rss_url'"
        self.results = None
        self.max_stories = max_stories
        self.story_intros = []
        self.story_intros.append(" .Next Story.  ")
        self.story_intros.append(" .This just in.  ")
        self.story_intros.append(" .Have you heard?.  ")
        self.story_intros.append(" .Up next.  ")

    def retrieve_rss(self, rss_url=None):
        rss_url_to_use = rss_url

        if rss_url_to_use is None:
            rss_url_to_use = self.rss_url

        if rss_url_to_use:
            url = string.Template(self.yql_rss_url).substitute({"rss_url": rss_url_to_use})
            #print("url: " + url)
            response = urllib.urlopen(url).read()
            self.results = json.loads(response)

    def generate_summary(self):
        news_entries = ""
        feed_title = ""
        news_summary = ""

        if self.results:
            max_limit = min(len(self.results['query']['results']['feed']), self.max_stories)

            for entry in self.results['query']['results']['feed'][:max_limit]:
                feed_title = entry['title']
                news_entries += self.story_intros[random.randint(0, 3)]
                news_entries += entry['entry']['title'] + '.  ' + entry['entry']['summary'] + '.  '
            news_summary = 'And now, The latest stories from the ' + feed_title + '.  ' + news_entries

        return news_summary

if __name__ == '__main__':
    y = YahooRss(rss_url="http://online.wsj.com/xml/rss/3_7041.xml")
    y.retrieve_rss()
    rss_summary = y.generate_summary()
    print(rss_summary)
    if platform.system() == 'Linux':
        from GoogleTextToSpeech import GoogleTextToSpeech

        script_dir = "/mnt/ram"
        g = GoogleTextToSpeech(tmp_dir = script_dir)
        g.get_text_to_speech(rss_summary)
        g.play_text_to_speech()
        g.clear_all()
