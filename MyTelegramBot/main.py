# -*- coding: utf-8 -*-
import weatherman as w
import mytranslator as t
import imageDescriber as icb
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

class BotSetting:
    def __init__(self):
        file = 'bot_token.txt'
        self.token = self.getToken(file)
        self.socks5 = {'proxy_url': 'socks5://lentach.gous32.ru:23202',
                        'urllib3_proxy_kwargs': {'username': 'lentach',
                                                 'password': 'pikcherbog11',
                                                }
                      }

        self.services = []

    def getToken(self, fileName):
        f = open(fileName)
        token = f.read()
        f.close()
        return token

    def appendService(self, service):
        self.services.append(service)

    def getFeaturesInfo(self):
        info = ''
        for s in self.services:
            info += s.description
        helpInfo  = '/help - узнать о моих способностях \n'
        startInfo = '/start - предупредить меня о начале работы \n'
        otherInfo = 'Я умею слышать Вас и повторять за Вами :) \n'
        info += helpInfo + startInfo + otherInfo
        return info

    def help(self, bot, update):
        infoText = self.getFeaturesInfo()
        bot.send_message(chat_id=update.message.chat_id, text=infoText)


    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="Привет, я твой личный ассистент Лэйн."
                              " Чтобы узнать, что я умею, напиши <</help>>!")


botSetting = BotSetting()
updater = Updater(token=botSetting.token, request_kwargs=botSetting.socks5)
dispatcher = updater.dispatcher

#Bot features
start_handler = CommandHandler('start', botSetting.start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', botSetting.help)
dispatcher.add_handler(help_handler)

translator = t.MyTranslator()
botSetting.appendService(translator)
translator_handler = CommandHandler(translator.commandT, translator.translate)
dispatcher.add_handler(translator_handler)
translator_handler = CommandHandler(translator.commandTS, translator.voiceTranslation)
dispatcher.add_handler(translator_handler)

weatherman = w.Weatherman()
botSetting.appendService(weatherman)
weatherman_handler = CommandHandler(weatherman.commandW, weatherman.getWeather)
dispatcher.add_handler(weatherman_handler)
weatherman_handler = CommandHandler(weatherman.commandWS, weatherman.voiceWeather)
dispatcher.add_handler(weatherman_handler)

imageDescriber = icb.ImageDescriber()
botSetting.appendService(imageDescriber)
imageDescriber_handler = MessageHandler(Filters.forwarded & Filters.photo | Filters.photo, imageDescriber.describeImg)
dispatcher.add_handler(imageDescriber_handler)

def weird(bot, update):
    answer = update.message.text
    if answer is None:
        answer = 'Я слышу тебя'
    bot.send_message(chat_id=update.message.chat_id, text=answer)

echo_handler = MessageHandler(Filters.voice | Filters.text, weird)
dispatcher.add_handler(echo_handler)

#Starts polling updates from Telegram
updater.start_polling()
