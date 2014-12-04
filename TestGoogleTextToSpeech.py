__author__ = 'youngsoul'

import GoogleTextToSpeech as tts
import os
import platform
import subprocess


script_dir = os.path.dirname(os.path.abspath(__file__))+"/tests/mp3files"
if platform.system() == "Linux":
    script_dir = "/mnt/ram"

g = tts.GoogleTextToSpeech(tmp_dir=script_dir)

g.get_text_to_speech("Your net worth is $123,456,789")
#g.get_text_to_speech("Welcome back my friends to the show that never ends.  Were so glad you could attend come inside, come inside")

print("mp3 file: " + os.path.abspath(g.mp3_files[0]))

if platform.system() == "Linux":
    # Play the mp3s returned
    print subprocess.call('mpg123 -h 10 -d 11 /mnt/ram/*.mp3', shell=True)
    #print subprocess.call('mpg123 -h 10 -d 11 '+os.path.abspath(mp3file), shell=True)
    print("finished playing mp3")
    print subprocess.call('rm /mnt/ram/*.mp3', shell=True)

g.clear_all()