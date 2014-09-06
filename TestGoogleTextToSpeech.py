__author__ = 'youngsoul'

import GoogleTextToSpeech as tts
import os
import platform
import subprocess


script_dir = os.path.dirname(os.path.abspath(__file__))

g = tts.GoogleTextToSpeech(tmp_dir=script_dir+"/tests/mp3files")

mp3file = g.get_text_to_speech("Your net worth is $4,125,345")

print("mp3 file: " + os.path.abspath(mp3file))

if platform.system() == "Linux":
    # Play the mp3s returned
    print subprocess.call('mpg123 -h 10 -d 11 '+os.path.abspath(mp3file), shell=True)
    print("finished playing mp3")
