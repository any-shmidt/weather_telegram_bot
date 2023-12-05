import telebot
from pyowm import OWM
from pyowm.utils import config
from telebot import types

from config import API_KEY, TOKEN

bot = telebot.TeleBot(token=TOKEN)


def get_weather_at_city(city):
    try:
        conf = config.get_default_config()
        conf['language'] = 'ru'

        owm = OWM(API_KEY, config=conf)
        mgr = owm.weather_manager()

        observation = mgr.weather_at_place(city)
        w = observation.weather

        detailed_status = w.detailed_status
        wind = round(w.wind()['speed'], 1)
        temp = round(w.temperature('celsius')['temp'])

        degree_celsius = '\u00B0'

        output = f'В городе {city} сейчас {detailed_status}\n'\
            f'Скорость ветра: {wind} м/c\n'\
            f'Температура: {temp}{degree_celsius}C'
    except:
        output = 'Ошибка! Такой город не найден.'

    return output


def get_city(message: types.Message):
    chat_id = message.chat.id
    city = message.text
    output = get_weather_at_city(city)
    bot.send_message(chat_id=chat_id, text=output)


@bot.message_handler(commands=['start', 'help'])
def info(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text='Чтобы узнать погоду в'\
        ' каком-либо городе, введите команду /weather')


@bot.message_handler(commands=['weather'])
def weather(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Введите название города')
    bot.register_next_step_handler(message, get_city)

if __name__ == '__main__':
    bot.infinity_polling()