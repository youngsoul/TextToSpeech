#!/usr/bin/env python

# Credit:  https://www.youtube.com/watch?v=julETnOLkaU
# modified to use this projects GoogleTextToSpeech and play
# mp3 files from an ordered playlist

import feedparser
import GoogleTextToSpeech as tts
import platform
import os
import subprocess


try:
    #
    # http://feeds.bbci.co.uk/news/world/rss.xml
    # Opinion: http://online.wsj.com/xml/rss/3_7041.xml
    # US Business: http://online.wsj.com/xml/rss/3_7014.xml
    # US Market News: http://online.wsj.com/xml/rss/3_7031.xml
    rss = feedparser.parse('http://online.wsj.com/xml/rss/3_7014.xml')


    # for entry in rss.entries[:4]:
    #     print entry['title']
    #     print entry['description']
#
#print rss.entries[0]['title']
#print rss.entries[0]['description']
#print rss.entries[1]['title']
#print rss.entries[1]['description']
#print rss.entries[2]['title']
#print rss.entries[2]['description']
#print rss.entries[3]['title']
#print rss.entries[3]['description']

    newsfeed = ""
    for entry in rss.entries[:5]:
        newsfeed += entry['title'] + '.  ' + entry['description'] + '.  '

# print newsfeed

# Today's news from BBC
#    news = 'And now, The latest stories from the World section of the BBC News.  ' + newsfeed
    news = 'And now, The latest stories from the ' + rss.feed.title + '.  ' + newsfeed

    print("News Summary: " + news)

    script_dir = os.path.dirname(os.path.abspath(__file__))+"/tests/mp3files"
    if platform.system() == "Linux":
        script_dir = "/mnt/ram"

    g = tts.GoogleTextToSpeech(tmp_dir=script_dir)
    g.get_text_to_speech(news)

    if platform.system() == "Linux":
        g.play_text_to_speech()
        g.clear()


except rss.bozo:
    news = 'Failed to reach BBC News'

# print news