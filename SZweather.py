# code: utf-8
import urllib.request, json, logging
from telegram.ext import Updater, CommandHandler  # MessageHandler, Filters


def main():
    updater = Updater(token='274017590:AAG0RbxIVTV62ZQpFRwMwIBgZGH_GICjlZE')
    dispatcher = updater.dispatcher
    szweather_handler = CommandHandler('sustech_weather', sustech_weather)
    dispatcher.add_handler(szweather_handler)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater.start_polling()


def sustech_weather(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="daf")  # getweather()


# get last location and print weather
def weather(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


# parameter to be changed
def getweather(location=None):
    url = 'http://wx.szmb.gov.cn/WeChat/map?lng=113.993088&lat=22.603228'
    response = urllib.request.urlopen(url)
    data = response.read()  # a `bytes` object
    text = data.decode('utf-8')  # a `str`; this step can't be used if data is binary
    info = json.loads(text)
    # output
    output = 'Data Time & Site Location: \n' + info['site'] + '\n'
    output += 'Temperature: ' + info['temp'] + '\n'
    output += 'WindSpeed:　' + info['wind'] + '\n'
    output += 'Humidity:　' + info['hum'] + '\n'
    output += 'Rain within 1 Hour:' + info['rain1H'] + '\n'
    output += 'Rain within 24 Hours: ' + info['rain24H'] + '\n'
    if info['forcast'] == []:
        output += 'No rain within 2 Hours.\n'
    else:
        output += '\n'.join(info['forcast'])
    return output


if __name__ == '__main__':
    main()
