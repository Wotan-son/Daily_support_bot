import logging
import os

import random
import requests
import telebot
from telebot import types
from dotenv import load_dotenv 

load_dotenv()

URL = 'https://api.thecatapi.com/v1/images/search'
URL_2 = 'https://api.thedogapi.com/v1/images/search'
MESSAGE = [
    'У тебя все получится!',
    'Я в тебя верю!',
    'Ты справишься!',
    'Все будет отлично!',
    'Это временные трудности!'
     
]
MESSAGE_2 = [
    'Ты очень красивая!',
    'Ты прекрасно выглядишь!',
    'Ты очаровательна!',
    'У тебя обворожительная улыбка!',
    'В твоих глазах бескрайний космос!'
]

secret_chat = os.getenv('TO_CHAT')
secret_token = os.getenv('TOKEN') 
bot = telebot.TeleBot(secret_token)

def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        bot.send_message('Все котики спят')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id,
                     "👋 Привет! Я твой бот! Пока я умею не так много, но у меня большой потенциал!",
                     reply_markup=markup)
    

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=None, row_width=2) #создание новых кнопок
        btn1 = types.KeyboardButton('Обзязательно нажми!')
        btn2 = types.KeyboardButton('Трудный день...')
        btn3 = types.KeyboardButton('Хочу кофе/чай/*на ручки*')
        btn4 = types.KeyboardButton('Время для котиков')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, 'Все просто - нажимаем на кпопку))', reply_markup=markup)
    
    elif message.text == 'Обзязательно нажми!':
        txt = random.choice(MESSAGE_2)
        bot.send_message(message.from_user.id, txt)
    elif message.text == 'Трудный день...':
        txt_2 = random.choice(MESSAGE)
        bot.send_message(message.from_user.id, txt_2)
    elif message.text == 'Хочу кофе/чай/*на ручки*':
        bot.forward_message(secret_chat, message.chat.id, message.message_id)
        bot.send_message(message.from_user.id, 'Отправил сообщение Славе')
    elif message.text == 'Время для котиков':
        photo = get_new_image()
        bot.send_photo(message.from_user.id, photo)

bot.polling(none_stop=True, interval=0)
