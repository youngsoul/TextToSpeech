__author__ = 'youngsoul'

import string
import urllib
import json
import platform
import random


class YahooRss:

    def __init__(self, rss_url=None, max_stories=7, summary_prefix='And now, The latest stories from the ', use_intros=True):
        self.rss_url = rss_url
        self.yql_rss_url = "https://query.yahooapis.com/v1/public/yql?format=json&q=SELECT title,entry.title,entry.summary.content FROM feednormalizer WHERE output='atom_1.0' AND url='$rss_url'"
        self.results = None
        self.max_stories = max_stories
        self.story_intros = []
        self.story_intros.append(" .Next Story.  ")
        self.story_intros.append(" .This just in.  ")
        self.story_intros.append(" .Have you heard?.  ")
        self.story_intros.append(" .Up next.  ")
        self.summary_prefix = summary_prefix
        self.use_intros = use_intros

    def retrieve_rss(self, rss_url=None):
        rss_url_to_use = rss_url

        if rss_url_to_use is None:
            rss_url_to_use = self.rss_url

        if rss_url_to_use:
            url = string.Template(self.yql_rss_url).substitute({"rss_url": rss_url_to_use})
            #print("url: " + url)
            response = urllib.urlopen(url).read()
            self.results = json.loads(response)

    def generate_summary(self, one_random_entry=False, space_title=False, wotd_title=False):
        """

        :param one_random_entry: True - if there are multiple entries, then just randomly pick one
        :param space_title: Add spaces to the title.  This was added because the acronym of
        the day, e.g. WTF, causes the speech generator to try to say the word instead of
        the letters.  Adding a space like, W T F causes the speech generator to say each
        letter.  True - add spaces, False - to not alter the title
        :param wotd_title: Changes the title to the format:
        <title>
        <title with spaces, so it sounds like it is spelled out>
        <title>
        This was added for word of the day functionality.
        :return:
        """
        news_entries = ""
        feed_title = ""
        news_summary = ""

        if self.results:
            max_limit = min(len(self.results['query']['results']['feed'])-1, self.max_stories)
            if max_limit > 1:
                all_entries = self.results['query']['results']['feed'][:max_limit]
            else:
                all_entries = [self.results['query']['results']['feed']]
            if one_random_entry:
                random_index = random.randint(0,len(all_entries)-1)
                all_entries = [all_entries[random_index]]

            for entry in all_entries:
                feed_title = entry['title']
                if self.use_intros:
                    news_entries += self.story_intros[random.randint(0, 3)]
                if wotd_title:
                    # useful for word of day
                    the_title = entry['entry']['title']
                    the_title += "  "
                    the_title += "  ".join(the_title)
                    the_title += " "
                    the_title += entry['entry']['title']
                    news_entries += the_title + '.  ' + entry['entry']['summary'] + '.  '
                else:
                    the_title = entry['entry']['title']
                    if space_title:
                        the_title = "  ".join(the_title)
                    news_entries += the_title + '.  ' + entry['entry']['summary'] + '.  '

            news_summary = self.summary_prefix + '  ' + feed_title + '.  ' + news_entries

        # if the aphostrophe is a special character, then replace it
        # with the ascii equivalent.
        return news_summary.replace(u'\u2019', "'")

if __name__ == '__main__':
    from BeautifulSoup import BeautifulSoup

    # http://xml.education.yahoo.com/rss/wotd/
    # {u'status': u'301', u'content': u'http://education.yahoo.com/rss/wotd/', u'from': u'http://xml.education.yahoo.com/rss/wotd/'}
    rss_url_wsj = "http://online.wsj.com/xml/rss/3_7041.xml"
    rss_url_wotd = "http://www.netlingo.com/feed-wotd.rss"
    rss_url_aotd = "http://www.netlingo.com/feed-aotd.rss"
    rss_url_wotd2 = "http://wordsmith.org/awad/rss2.xml"
    rss_url_wotd3 = "http://www.merriam-webster.com/wotd/feed/rss2"

    rss_url_history = "http://feeds.feedburner.com/historyorb/todayinhistory?format=xml"

    y = YahooRss(rss_url=rss_url_wotd2, max_stories=20, summary_prefix="", use_intros=False)
    y.retrieve_rss()
    rss_summary = y.generate_summary(one_random_entry=False, space_title=False, wotd_title=True)

    rss_summary = BeautifulSoup(rss_summary).getText(" ")
    #rss_summary = rss_summary.replace("For more info, visit the link below!","")

    print(rss_summary)
    if platform.system() == 'Linux':
        from GoogleTextToSpeech import GoogleTextToSpeech

        script_dir = "/mnt/ram"
        g = GoogleTextToSpeech(tmp_dir = script_dir)
        g.get_text_to_speech(rss_summary)
        g.play_text_to_speech()
        g.clear_all()
