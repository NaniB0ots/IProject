import json

from project.settings import TG_TOKEN
from tg_bot import core, models
from tg_bot.core import Bot
from tg_bot.utils import keyboards

if not TG_TOKEN:
    raise ValueError('TG_TOKEN не может быть пустым')

bot = Bot(TG_TOKEN)


# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    user = core.User(chat_id)

    if not user.object:
        bot.send_message(chat_id=chat_id, text=bot.get_start_message())
        msg = bot.send_authorization_message(chat_id=chat_id)
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_message(chat_id=chat_id, text=bot.get_start_message(), reply_markup=keyboards.get_main_menu_keyboard())


def authorization(message):
    chat_id = message.chat.id
    token = message.text
    username = message.from_user.username
    user = core.User(chat_id)
    if user.authorization(token=token, username=username):
        bot.send_message(chat_id=chat_id, text=bot.get_instruction(), reply_markup=keyboards.get_main_menu_keyboard())
    else:
        msg = bot.send_authorization_message(chat_id)
        bot.register_next_step_handler(msg, authorization)


@bot.message_handler(regexp='^Профиль$')
def profile(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.object:
        msg = bot.send_authorization_message(chat_id)
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_message(chat_id=chat_id, text=user.get_user_info_text(),
                     reply_markup=keyboards.get_inline_profile_keyboard(), parse_mode='html')


@bot.message_handler(regexp='^Поиск$')
def search_menu(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.object:
        msg = bot.send_authorization_message(chat_id)
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_message(chat_id=chat_id, text='Меню поиска',
                     reply_markup=keyboards.get_search_menu_keyboard(), parse_mode='html')


@bot.message_handler(regexp='^Основное меню$')
def main_menu(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.object:
        msg = bot.send_authorization_message(chat_id)
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_message(chat_id=chat_id, text='Основное меню',
                     reply_markup=keyboards.get_main_menu_keyboard(), parse_mode='html')


@bot.message_handler(regexp='^Мои проекты$')
def main_menu(message):
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.object:
        msg = bot.send_authorization_message(chat_id)
        bot.register_next_step_handler(msg, authorization)
        return

    projects = core.Project.get_projects_by_user(user_profile=user.object.student_profile)
    if not projects:
        bot.send_message(chat_id=chat_id, text='У Вас нет активныйх проектов🥺\n\n'
                                               'Воспользуйтесь поиском, чтобы найти проект для себя☺️\n')
        return

    for project in projects:
        bot.send_message(chat_id=chat_id, text=core.Project.get_project_info_str(project),
                         reply_markup=keyboards.get_main_menu_keyboard(), parse_mode='html')


@bot.message_handler(
    content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def invalid_message(message):
    """
    Ответ на текст, который бот не понимает.
    Функция должна быть последней по порядку!
    :return:
    """
    chat_id = message.chat.id
    user = core.User(chat_id)
    if not user.object:
        msg = bot.send_authorization_message(chat_id)
        bot.register_next_step_handler(msg, authorization)
        return

    bot.send_invalid_message_answer(chat_id=chat_id)
