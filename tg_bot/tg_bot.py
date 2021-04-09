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
