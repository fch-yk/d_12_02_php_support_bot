import textwrap

from telegram import ReplyKeyboardMarkup, KeyboardButton
from .models import RegistrationRequest

def show_auth_keyboard(update, context):
    message = textwrap.dedent('''
        Перед началом использования необходимо зарегистрироваться.
        Пожалуйста, выберите свою роль:''')

    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("🔐 Получить доступ клиента")],
         [KeyboardButton("🔐 Получить доступ исполнитель")], ],
        resize_keyboard=True
    )
    update.message.reply_text(text=message, reply_markup=reply_markup)


