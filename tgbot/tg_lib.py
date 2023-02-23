import textwrap

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def show_auth_keyboard(update, context):
    message = textwrap.dedent('''
        Перед началом использования необходимо зарегистрироваться.
        Пожалуйста, выберите свою роль:''')

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔐 Получить доступ клиента", callback_data='client_auth')],
         [InlineKeyboardButton("🔐 Получить доступ исполнителя", callback_data='contracter_auth')], ],
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
