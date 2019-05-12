from captionbot import CaptionBot
from googletrans import Translator

class ImageDescriber:
    def __init__(self):
        self.captionBot = CaptionBot() #www.captionbot.ai
        self.translator = Translator()
        self.dest = 'ru'
        self.description = 'send_photo - Я могу рассказать, что изображено на картинке \n'

    def describeImg(self, bot, update):
        imgId = update.message.photo[-1]
        imgPath = bot.getFile(imgId)
        imgPath = imgPath['file_path']
        caption = self.getImageCaption(imgPath)
        bot.send_message(chat_id=update.message.chat_id, text=caption)

    def getImageCaption(self, imgPath):
        caption = self.captionBot.url_caption(imgPath)
        caption = self.translator.translate(caption, dest=self.dest).text
        return caption

