from telebot import types
import json

MAX_CALLBACK_RANGE = 41


def get_main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Мои проекты')
    btn2 = types.KeyboardButton('Профиль')
    btn3 = types.KeyboardButton('Настройки')
    btn4 = types.KeyboardButton('Другое')

    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4)
    return markup


def get_inline_authorization_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Профиль', url='https://vk.com/'))
    return markup
