__author__ = 'youngsoul'

import platform
import os


if __name__ == '__main__':
    from GoogleTextToSpeech import GoogleTextToSpeech
    script_dir = os.path.dirname(os.path.abspath(__file__))+"/tests/mp3files"
    if platform.system() == 'Linux':
        script_dir = "/mnt/ram"

    g = GoogleTextToSpeech(tmp_dir = script_dir)

    messages = []
    messages.append("Your most recent blood glucose was 140, and you took 430 steps yesterday.  ")
    messages.append("Make sure you stay active today and make healthy meal choices.  ")
    messages.append("Have a great day and dont forget to check your blood sugar.")

    summary = messages[0] + messages[1] + messages[2]
    g.get_text_to_speech(summary)
    if platform.system() == 'Linux':
        g.play_text_to_speech()
    g.clear_play_list()
