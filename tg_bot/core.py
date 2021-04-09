import telebot
import datetime

from django.conf import settings
from django.utils import timezone, dateformat

from tg_bot import models
from tg_bot.utils import keyboards
from threading import Thread

from project_manager import models as project_manager_models


class Bot(telebot.TeleBot):
    @staticmethod
    def get_start_message() -> str:
        message = 'Добрейшего времени суток!\n' \
                  'Тебя приветствует менеджер проектной деятельности ИРНИТУ.\n' \
                  'Добро пожаловать!'

        return message

    @staticmethod
    def get_list_of_commands() -> str:
        message = '/start - запустить бота'

        return message

    def send_invalid_message_answer(self, chat_id):
        text = 'Я Вас не понимаю. Воспользуйтесь клавиатурой'
        self.send_message(chat_id=chat_id, text=text, reply_markup=keyboards.get_main_menu_keyboard())

    @staticmethod
    def get_instruction() -> str:
        text = '<Инструкция по пользованию ботом...>'
        return text

    def send_message_to_all_users(self, text):
        pass

    def send_authorization_message(self, chat_id):
        text = 'Для того чтобы начать пользоваться функциями бота, отправьте боту токен авторизации.\n\n ' \
               'Токен можно получить в личном кабинете'

        msg = self.send_message(chat_id=chat_id, text=text, reply_markup=keyboards.get_inline_authorization_keyboard())
        return msg


class User:
    model = models.TgUser

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.object = self.get_object()

    def get_object(self):
        try:
            return self.model.objects.get(chat_id=self.chat_id)
        except self.model.DoesNotExist:
            return self.model.objects.none()

    def authorization(self, token: str, username: str):
        try:
            user_profile = project_manager_models.Student.objects.get(authorization_token__token=token)
        except project_manager_models.Student.DoesNotExist:
            return self.model.objects.none()

        return self.model.objects.create(chat_id=self.chat_id, username=username, student_profile=user_profile)
