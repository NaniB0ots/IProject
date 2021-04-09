from telebot import types
import json

from project.settings import PROFILE_URL, PROJECT_URL

MAX_CALLBACK_RANGE = 41


def get_main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Мои проекты')
    btn2 = types.KeyboardButton('Профиль')
    btn3 = types.KeyboardButton('Поиск')
    btn4 = types.KeyboardButton('Другое')

    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4)
    return markup


def get_inline_profile_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Личный кабинет', url=PROFILE_URL))
    return markup


def get_search_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Поиск ментора')
    btn2 = types.KeyboardButton('Поиск оборудования')
    btn3 = types.KeyboardButton('Поиск аудитории')
    btn4 = types.KeyboardButton('Основное меню')

    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4)
    return markup


def get_inline_project_card_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Карточка проекта', url=PROJECT_URL))
    return markup
