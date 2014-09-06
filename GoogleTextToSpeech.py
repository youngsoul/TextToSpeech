__author__ = 'youngsoul'

import os
import hashlib
import base64
import requests
import textwrap



#
# I know this has been answered already,
# but I discovered a more general solution in case anyone is interested -
# you can pass a more specific locale in the tl parameter, e.g.
#
# http://translate.google.com/translate_tts?q=testing+1+2+3&tl=en_us
#
# http://translate.google.com/translate_tts?q=testing+1+2+3&tl=en_gb
#
# http://translate.google.com/translate_tts?q=testing+1+2+3&tl=en_au


class GoogleTextToSpeech:

    def __init__(self, tmp_dir="/mnt/ram"):
        self.tts_url = "http://translate.google.com/translate_tts?tl=en_gb&q="
        self.tmp_dir = tmp_dir
        self.mp3_files = []

    def _save_playlist(self):
        if len(self.mp3_files) > 0:
            with open(self.tmp_dir + "/play_list.txt", 'w')as f:
                f.writelines(self.mp3_files)
                f.flush()


    #
    # Download url to a file that is the base64(md5(url))[file extension]
    # for exmple:
    # "http://www.schillmania.com/projects/soundmanager2/demo/_mp3/rain.mp3"
    # is converted to:
    # ZmZiOWE2YmMxYmY1NzdmNzQzODUxMTNkNjcxODhlOTI=.mp3
    #
    def _download_file(self, text_sample):
        local_filename = self._create_media_filename(text_sample)

        self.mp3_files.extend(local_filename+"\n")

        if not os.path.isfile(local_filename):
            # local_filename = url.split('/')[-1]
            # NOTE the stream=True parameter
            the_url = self.tts_url+"'"+text_sample+"'"
            print("url: " + the_url)
            r = requests.get(the_url, stream=True)
            with open(local_filename, 'wb')as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
        return local_filename

    @staticmethod
    def _create_base64_md5_hash(string_to_hash):
        string_to_hash_as_bytes = unicode.encode(string_to_hash)
        md5_hash_string = hashlib.md5(string_to_hash_as_bytes).hexdigest()
        md5_as_base64_bytes = base64.standard_b64encode(str.encode(md5_hash_string))
        md5_as_base64_string = md5_as_base64_bytes.decode('ascii')
        return md5_as_base64_string

    def _create_media_filename(self, text_sample):
        # create a md5 hash of url to use as filename, and check to see
        # if that file is already available
        md5_text_hash = GoogleTextToSpeech._create_base64_md5_hash(text_sample)
        local_filename = self.tmp_dir + "/" + md5_text_hash + ".mp3"
        return local_filename

    def get_text_to_speech(self, text_sample):
        self.mp3_files = []
        if len(text_sample) > 100:
            shorts = []
            for chunk in text_sample.split('. '):
                shorts.extend(textwrap.wrap(chunk, 100))

            for sentence in shorts:
                self._download_file(sentence.lstrip())

        else:
            self._download_file(text_sample)

        self._save_playlist()