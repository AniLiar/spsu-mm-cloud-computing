import requests
import mytranslator as t

class Weatherman:
    def __init__(self):
        #https://habr.com/ru/post/315264/
        file = 'weatherman_token.txt'
        self.token = self.getToken(file)
        self.lang = 'ru'
        self.api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=%(token)s&lang=%(lang)s&q=' % \
                           {"token":  self.token, 'lang': self.lang}
        self.commandW = 'w'
        self.lengthCommandW = len(self.commandW) + 1  # commandW = '/w'
        self.commandWS = 'ws'
        self.lengthCommandWS = len(self.commandWS) + 1  # commandWS = '/ws'
        self.translator = t.MyTranslator()
        self.description = '/w Name_city - узнать погоду в городе Name_city \n' \
                           '/ws Name_city - озвучить погоду в городе Name_city \n'

    def getToken(self, fileName):
        f = open(fileName)
        token = f.read()
        f.close()
        return token

    def kelvinToCelsius(self, degreeK):
        degreeC = degreeK - 273.15
        return round(degreeC)

    def getWeather(self, bot, update):
        city = update.message.text[self.lengthCommandW:]
        if city is None:
            bot.send_message(chat_id=update.message.chat_id, text="Пожалуйста, напиши <</w Name_city>>!")
        try:
            weather = self.getWeatherFromApi(city)
            bot.send_message(chat_id=update.message.chat_id, text=weather)
        except Exception:
            bot.send_message(chat_id=update.message.chat_id, text="Ой, я не нашла такого города, повтори, пожалуйста :)")


    def voiceWeather(self, bot, update):
        city = update.message.text[self.lengthCommandWS:]
        if city is None:
            bot.send_message(chat_id=update.message.chat_id, text="Пожалуйста, напиши <</w Name_city>>!")
        try:
            weather = self.getWeatherFromApi(city, doMore = True)
            voicePath = self.translator.translateTextToSpeech(weather)
            bot.send_voice(chat_id=update.message.chat_id, voice=open(voicePath, 'rb'))
        except Exception:
            bot.send_message(chat_id=update.message.chat_id, text="Ой, я не нашла такого города, повтори, пожалуйста :)")

    # def translate(self, phrase, dest='ru'):
    #     translation = self.translator.translatePhrase(phrase, dest=dest)
    #     return translation.text

    def formStringWithWeather(self, city, description, minTemp, maxTemp, doMore):
        degreeSign = u'\N{DEGREE SIGN}C'
        weatherDetails = {"city": city, 'description': description,
                           "minTemp": minTemp, "maxTemp": maxTemp, "degree": degreeSign}
        if doMore:
            weather = 'Погода в городе %(city)s: %(description)s, температура ' \
                      'от %(minTemp)d %(degree)s до %(maxTemp)d %(degree)s' % \
                      weatherDetails
        else:
            weather = 'Погода в городе %(city)s: \n %(description)s \n ' \
                      '%(minTemp)d %(degree)s / %(maxTemp)d %(degree)s' % \
                      weatherDetails
        return weather

    def getWeatherFromApi(self, city, doMore = False):
        cityEng = self.translator.translatePhrase(city, 'en')
        url = self.api_address + cityEng
        json_data = requests.get(url).json()
        description = json_data['weather'][0]['description']
        maxTemp = self.kelvinToCelsius(json_data['main']['temp_max'])
        minTemp = self.kelvinToCelsius(json_data['main']['temp_min'])

        weather = self.formStringWithWeather(city, description, minTemp, maxTemp, doMore)
        return weather