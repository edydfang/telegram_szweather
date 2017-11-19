#!/usr/bin/env python3
#  code: utf-8
import urllib.request, json, logging
import urllib.error
import sys
from telegram.ext import Updater, CommandHandler  # MessageHandler, Filters

DEBUG_MODE = False

def main():
    TOKEN = "274017590:AAHwfPetzzkUdfdUtK--L1M793bj2TiwRbk"
    logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.info("Start Servering...")
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    weather_handler = CommandHandler('sustech_weather', sustech_weather)
    forcast_handler = CommandHandler('sustech_forecast', sustech_forecast)
    dispatcher.add_handler(weather_handler)
    dispatcher.add_handler(forcast_handler)
    logging.info("Start Polling...")
    if DEBUG_MODE:
        updater.start_polling()
    else:
        '''
        just for heroku
       '''
        import os
        PORT = int(os.environ.get('PORT', '5000'))
        # add handlers
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://telegram-weather.herokuapp.com/" + TOKEN)
        updater.idle()
    # end heroku


def sustech_forecast(bot, update):
    logging.info("Received command.")
    bot.sendMessage(chat_id=update.message.chat_id, text=getforecast())  # getweather()
    logging.info("Send successfully.")

def get_API_data(location=(22.597700, 114.000110)):
    url = 'http://wx.szmb.gov.cn/MobileWeather/position/query?latitude=%.6f&longitude=%.6f' % location
    response = urllib.request.urlopen(url)
    data = response.read()  # a `bytes` object
    text = data.decode('utf-8')  # a `str`; this step can't be used if data is binary
    info = json.loads(text)
    return info

def sustech_weather(bot, update):
    logging.info("Received command.")
    bot.sendMessage(chat_id=update.message.chat_id, text=getweather())  # getweather()
    logging.info("Send successfully.")


# get last location and print weather
def weather(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def getweather(location=(22.597700, 114.000110)):
    # new api js example http://wx.szmb.gov.cn/MobileWeather/script/nadforecastv1.js
    info = get_API_data(location)
    try:
        # output
        output = 'Update Time %s\n' % info['dataTimeFormat']
        output += 'Site Location: %s\n' % info['content']
        output += 'Weather Now: %s\n' % info['forecast']
        output += u'Tempature Now: %s\u2103\n' % info['temp']
        output += 'Humidity: %s%%\n' % info['humidity']
        output += 'Rain within 1 Hour: %s mm\n' % info['r01h']
        output += 'Rain within 3 Hours: %s mm\n' % info['r03h']
        output += 'Wind: %s\n' % info['windStr']
    except (KeyError,urllib.error.HTTPError):
        logging.info("Weather querying failed.")
        output = "Sorry, weather querying failed."


    return output

# parameter to be changed
def getforecast(location=(22.597700, 114.000110)):
    # new api js example http://wx.szmb.gov.cn/MobileWeather/script/nadforecastv1.js
    info = get_API_data(location)
    output = "Weather Forecast for next week:"
    try:
        # output
        for day in info['week']:
            newline = "[%s %s]\nTemp: %s~%s\u2103\nWeather:%s\n" \
                      % (day['formatTime'], day['week'], day['minTemp'], day['maxTemp'], day['weather'])
            output += newline
    except KeyError:
        logging.info("Weather querying failed.")
        output = "Sorry, weather querying failed."
    return output


if __name__ == '__main__':
    main()
