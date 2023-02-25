import textwrap

from telegram import ReplyKeyboardMarkup, KeyboardButton
from .models import RegistrationRequest

def show_auth_keyboard(update, context):
    message = textwrap.dedent('''
        Добрый день! Я PHP support бот. Принимаю заказы от клиентов по доработкам сайтов на PHP. Ищу подрядчиков на выполнение этих работ.
        Перед началом использования необходимо зарегистрироваться.
        Пожалуйста, выберите свою роль: ...
    ''')

    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("🔐 Получить доступ клиента")],
         [KeyboardButton("🔐 Получить доступ подрядчика")], ],
        resize_keyboard=True
    )
    update.message.reply_text(text=message, reply_markup=reply_markup)


def show_client_menu_keyboard(update, context, client_name):
    message = f'Добрый день {client_name}! Выберите дальнейшую команду.'

    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("Оформить новую заявку")],
         [KeyboardButton("Список моих заявок")], ],
        resize_keyboard=True
    )
    update.message.reply_text(text=message, reply_markup=reply_markup)

def show_subcontractor_menu_keyboard(update, context, client_name):
    message = f'Добрый день {client_name}! Выберите дальнейшую команду.'

    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("Список новых заявок")],
         [KeyboardButton("Мои заявки")], ],
        resize_keyboard=True
    )
    update.message.reply_text(text=message, reply_markup=reply_markup)

def show_subcontractor_order_keyboard(update, context, client_name):
    message = f'Добрый день {client_name}! Выберите дальнейшую команду.'

    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("Изменить статус заявки")],
         [KeyboardButton("Назад")], ],
        resize_keyboard=True
    )
    update.message.reply_text(text=message, reply_markup=reply_markup)

def show_client_order_keyboard(update, context, client_name):
    message = f'Список Ваших заявок. Выберите дальнейшее действие'

    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("Внести изменение в заявку")],
         [KeyboardButton("Назад")], ],
        resize_keyboard=True
    )
    update.message.reply_text(text=message, reply_markup=reply_markup)
