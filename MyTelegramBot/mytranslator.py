from googletrans import Translator
from gtts import gTTS

class MyTranslator:
    def __init__(self):
        self.translator = Translator()
        self.commandT = 't'
        self.lengthCommandT = len(self.commandT ) + 1 #command = '/t'
        self.commandTS = 'ts'
        self.lengthCommandTS = len(self.commandTS) + 1  # command = '/t'
        self.dest = 'ru'
        self.description = '/t phrase - перевести phrase с любого языка на русский \n' \
                           '/ts phrase - перевести phrase с любого языка на русский и озвучить \n'


    def translate(self, bot, update):
        phrase = update.message.text[self.lengthCommandT:]
        translation = self.translatePhrase(phrase, dest=self.dest)
        bot.send_message(chat_id=update.message.chat_id, text=translation)

    def translatePhrase(self, phrase, dest='ru'):
        translation = self.translator.translate(phrase, dest=dest)
        return translation.text

    def voiceTranslation(self, bot, update):
        phrase = update.message.text[self.lengthCommandTS:]
        translation = self.translatePhrase(phrase, dest=self.dest)
        voicePath = self.translateTextToSpeech(translation)
        bot.send_voice(chat_id=update.message.chat_id, voice=open(voicePath, 'rb'))

    def translateTextToSpeech(self, text):
        tts = gTTS(text=str(text), lang="ru")
        fileName = "speach.ogg"
        tts.save(fileName)
        return fileName