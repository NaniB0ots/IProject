import telebot
import datetime

from django.conf import settings
from django.utils import timezone, dateformat

from tg_bot import models
from tg_bot.utils import keyboards
from threading import Thread


class Bot(telebot.TeleBot):
    @staticmethod
    def get_start_message() -> str:
        message = 'Добрейшего времени суток!\n\n' \
                  'Тебя приветствует менеджер проектной деятельности ИРНИТУ.\n\n' \
                  'Добро пожаловать!'

        return message

    @staticmethod
    def get_list_of_commands() -> str:
        message = '/start - запустить бота'

        return message

    def send_invalid_message_answer(self, chat_id):
        text = 'Я Вас не понимаю. Воспользуйтесь клавиатурой'
        self.send_message(chat_id=chat_id, text=text, reply_markup=keyboards.get_main_menu_keyboard())

    def send_message_to_all_users(self, text):
        pass