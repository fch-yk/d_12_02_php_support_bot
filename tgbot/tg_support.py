import os
import textwrap

from dotenv import load_dotenv

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

from telegram.ext import Updater, Filters
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler


def show_auth_keyboard(update, context):
    message = textwrap.dedent('''
        Перед началом использования необходимо зарегистрироваться.
        Пожалуйста, выберите свою роль:''')

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔐 Получить доступ клиента", callback_data='client_auth')],
         [InlineKeyboardButton("🔐 Получить доступ исполнителя", callback_data='contracter_auth')],],
        resize_keyboard=True
    )
    update.message.reply_text(text=message, reply_markup=reply_markup)


def show_registration_keyboard(update, context):
    query = update.callback_query
    if query.data == 'client_auth':
        message = textwrap.dedent('''
            Напишите название вашей компании и контакную информацию
            В ближайшее время наш менеджер свяжется с Вами''')
    else:
        message = textwrap.dedent('''
            Напишите немного о себе (резюме)
            В ближайшее время наш менеджер свяжется с Вами''')

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("✅ Отправить заявку", callback_data='send_request')]],
    )
    update.callback_query.message.reply_text(text=message, reply_markup=reply_markup)


def start(update, context):
    show_auth_keyboard(update, context)
    return "HANDLE_MENU"


def handle_auth(update, context):
    show_registration_keyboard(update, context)
    return 'HANDLE_NEW_USER'


def handle_users_reply(update, context):
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return

    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = 'HANDLE_AUTH'

    states_functions = {
        'START': start,
        'HANDLE_AUTH': handle_auth,
        'HANDLE_NEW_USER': handle_auth,
        # 'HANDLE_CART': view_cart,
        # 'WAITING_EMAIL': waiting_email,
    }

    state_handler = states_functions[user_state]
    try:
        next_state = state_handler(update, context)
        # db.set(chat_id, next_state)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    load_dotenv()
    token = os.environ.get("TELEGRAM_TOKEN")
    client_id = os.environ.get("CLIENT_ID")


    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))

    updater.start_polling()


