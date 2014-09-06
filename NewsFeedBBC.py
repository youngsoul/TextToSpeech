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
    rss = feedparser.parse('http://feeds.bbci.co.uk/news/world/rss.xml')


#for entry in rss.entries[:4]:
#    print entry['title']
#    print entry['description']
#
#print rss.entries[0]['title']
#print rss.entries[0]['description']
#print rss.entries[1]['title']
#print rss.entries[1]['description']
#print rss.entries[2]['title']
#print rss.entries[2]['description']
#print rss.entries[3]['title']
#print rss.entries[3]['description']

    newsfeed = rss.entries[0]['title'] + '.  ' + rss.entries[0]['description'] + '.  ' + rss.entries[1]['title'] + '.  ' + rss.entries[1]['description'] + '.  ' + rss.entries[2]['title'] + '.  ' + rss.entries[2]['description'] + '.  ' + rss.entries[3]['title'] + '.  ' + rss.entries[3]['description'] + '.  '

# print newsfeed

# Today's news from BBC
    news = 'And now, The latest stories from the World section of the BBC News.  ' + newsfeed

    script_dir = os.path.dirname(os.path.abspath(__file__))+"/tests/mp3files"
    if platform.system() == "Linux":
        script_dir = "/mnt/ram"

    g = tts.GoogleTextToSpeech(tmp_dir=script_dir)
    g.get_text_to_speech(news)

    if platform.system() == "Linux":
        play_list_file = script_dir + "/play_list.txt"
        # Play the mp3s returned
        print subprocess.call('mpg123 -h 10 -d 11 --list ' + play_list_file, shell=True)
        #print subprocess.call('mpg123 -h 10 -d 11 '+os.path.abspath(mp3file), shell=True)
        print("finished playing mp3")
        print subprocess.call('rm /mnt/ram/*.mp3', shell=True)
        print subprocess.call('rm /mnt/ram/*.txt', shell=True)


except rss.bozo:
    news = 'Failed to reach BBC News'

# print news