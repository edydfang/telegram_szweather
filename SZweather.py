#!/usr/bin/env python3
#  code: utf-8
import urllib.request, json, logging
import sys
from telegram.ext import Updater, CommandHandler  # MessageHandler, Filters



def main():
    logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.info("Start Servering...")
    updater = Updater(token='274017590:AAHwfPetzzkUdfdUtK--L1M793bj2TiwRbk')
    dispatcher = updater.dispatcher
    szweather_handler = CommandHandler('sustech_weather', sustech_weather)
    dispatcher.add_handler(szweather_handler)
    logging.info("Start Polling...")
    #updater.start_polling()
    '''
    just for heroku
    '''
    import os
    TOKEN = "274017590:AAHwfPetzzkUdfdUtK--L1M793bj2TiwRbk"
    PORT = int(os.environ.get('PORT', '5000'))
    updater = Updater(TOKEN)
    # add handlers
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://telegram-weather.herokuapp.com/" + TOKEN)
    updater.idle()
    # end heroku


def sustech_weather(bot, update):
    logging.info("Received command.")
    bot.sendMessage(chat_id=update.message.chat_id, text=getweather())  # getweather()
    logging.info("Send successfully.")


# get last location and print weather
def weather(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


# parameter to be changed
def getweather(location=None):
    # new api js example http://wx.szmb.gov.cn/MobileWeather/script/nadforecastv1.js
    url = 'http://wx.szmb.gov.cn/MobileWeather/position/query?latitude=22.597700&longitude=114.000110'
    output = ""
    try:
        response = urllib.request.urlopen(url)
        data = response.read()  # a `bytes` object
        text = data.decode('utf-8')  # a `str`; this step can't be used if data is binary
        info = json.loads(text)
        # output
        output = 'Update Time %s\n' % info['dataTimeFormat']
        output = 'Site Location: %s\n' % info['content']
        output += 'Forcast: %s\n' % info['forecast']
        output += 'Tempature Now: %s\n' % info['temp']
        output += 'Humidity: %s%%\n' % info['humidity']
        output += 'Rain within 1 Hour: %s\n' % info['r01h']
        output += 'Rain within 3 Hours: %s\n' % info['r03h']
        output += 'Wind: %s\n' % info['windStr']
    except KeyError:
        logging.info("Weather querying failed.")
        output = "Sorry, weather querying failed."
    return output


if __name__ == '__main__':
    main()
