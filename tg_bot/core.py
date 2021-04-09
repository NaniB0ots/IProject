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

    @staticmethod
    def get_instruction() -> str:
        text = '<Инструкция по пользованию ботом...>'
        return text

    def send_message_to_all_users(self, text):
        pass

    def send_authorization_message(self, chat_id):
        text = 'Для того чтобы начать пользоваться функциями бота, введите токен авторизации.\n\n ' \
               'Токен можно получить в профиле'

        msg = self.send_message(chat_id=chat_id, text=text, reply_markup=keyboards.get_inline_authorization_keyboard())
        return msg


class User:
    model = models.TgUser

    def __init__(self):
        self.object = self.get_object()

    def get_object(self):
        try:
            return self.model.objects.get()
        except self.model.DoesNotExist:
            return self.model.objects.none()

    def authorization(self, chat_id: int, token: str, username: str):

        try:
            token_object = project_manager_models.AuthorizationToken.objects.get(token=token, is_used=False)
        except project_manager_models.AuthorizationToken.DoesNotExist:
            return self.model.objects.none()
        token_object.is_used = True
        token_object.save()
        return self.model.objects.create(chat_id=chat_id, token=token, username=username)
