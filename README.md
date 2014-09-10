TextToSpeech
============

Python Library for text to speech testing

Sample project to generate mp3 files from googles translate service and play the mp3 on a raspberry pi through the audio out channel.

Inspired heavily by this youtube project:

https://www.youtube.com/watch?v=julETnOLkaU

GoogleTextToSpeech.py
Class interfaces to the google translate services.  This class will create a hash out of the
string to get speech for so that if you ask for the same string again, it can avoid a trip to the
google services - assuming you did not remove the files.

This implementation also uses a playlist file to order the mp3 files correctly if you exceed the
100 character limitation from google.

For the Yahoo classes, the idea is that the method generate_summary would be re-implemented by anyone
that wanted it to say something different, but the other methods would still be useful for
the interaction to the service.

