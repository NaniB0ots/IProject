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

        msg = self.send_message(chat_id=chat_id, text=text, reply_markup=keyboards.get_inline_profile_keyboard())
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

    def get_user_info_text(self) -> str:
        if not self.object:
            return 'Произошла ошибка. Попробуйте позже...'
        firstname = self.object.student_profile.firstname
        last_name = self.object.student_profile.lastname
        patronymic = self.object.student_profile.patronymic
        group = self.object.student_profile.group
        tags = self.object.student_profile.tags.all()

        tags_str = ''
        for tag in tags:
            tags_str += f'<i>{tag.tag}</i>, '
        tags_str = tags_str[:-2]  # обрезаем запятую

        text = f'<b>{last_name} {firstname} {patronymic if patronymic else ""}</b>\n' \
               f'Группа: {group}\n' \
               f'Интересы: {tags_str if tags_str else "пусто..."}\n\n' \
               f'Интересы можно изменить в личном кабинете'

        return text


class Project:
    @staticmethod
    def get_projects_by_user(user_profile):
        return project_manager_models.Project.objects.filter(students=user_profile)

    @staticmethod
    def get_students_info(students: project_manager_models.Student.objects) -> str:
        composition = ''
        for student in students:

            firstname = student.firstname
            last_name = student.lastname
            patronymic = student.patronymic
            group = student.group
            tags = student.tags.all()

            student_tags_str = ''
            for tag in tags:
                student_tags_str += f'<i>{tag.tag}</i>, '
            student_tags_str = student_tags_str[:-2]  # обрезаем запятую

            student_info = f'{" " * 5}{last_name} {firstname} {patronymic if patronymic else ""}\n' \
                           f'{" " * 5}Группа: {group}\n' \
                           f'{" " * 5}Интересы: {student_tags_str if student_tags_str else "пусто..."}'
            composition += f'{student_info}\n\n'
        return composition

    @staticmethod
    def get_manager_info(manager: project_manager_models.Teacher) -> str:
        if not manager:
            return ''
        firstname = manager.firstname
        last_name = manager.lastname
        patronymic = manager.patronymic
        post = manager.post
        tags = manager.tags.all()

        tags_str = ''
        for tag in tags:
            tags_str += f'<i>{tag.tag}</i>, '
        tags_str = tags_str[:-2]  # обрезаем запятую

        text = f'{" " * 5}{last_name} {firstname} {patronymic if patronymic else ""}\n' \
               f'{" " * 5}Должность: {post}\n' \
               f'{" " * 5}Компетенции: {tags_str if tags_str else "..."}'

        return text

    @classmethod
    def get_project_info_str(cls, project: project_manager_models.Project) -> str:
        tags = project.tags.all()
        students = project.students.all()

        tags_str = ''
        for tag in tags:
            tags_str += f'<i>{tag.tag}</i>, '
        tags_str = tags_str[:-2]  # обрезаем запятую

        manager_info = cls.get_manager_info(manager=project.teacher)
        composition = cls.get_students_info(students)

        text = f'<b>{project.title}</b>\n' \
               f'{project.description}\n\n' \
               f'Сложность: <b>{project.difficulty}</b>\n' \
               f'Направления: <i>{tags_str}</i>\n\n' \
               f'<b>Руководитель:</b>\n' \
               f'{manager_info if manager_info else "..."}\n\n' \
               f'<b>Проектная команда:\n</b>' \
               f'{composition}'

        return text
