__author__ = 'youngsoul'


from GoogleTextToSpeech import GoogleTextToSpeech

g = GoogleTextToSpeech()

g.tmp_dir = "/Users/youngsoul/Documents/Development/PythonDev/TextToSpeech/tests/mp3files"

mp3file = g.get_text_to_speech("Your net worth is $125,345")

