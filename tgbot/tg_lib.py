import textwrap
import datetime

from telegram import ReplyKeyboardMarkup, KeyboardButton
from .models import Subscription, Order, Subcontractor

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

def show_subcontractor_menu_keyboard(update, context):
    message = f'Выберите дальнейшую команду.'

    subcontractor = Subcontractor.objects.get(telegram_user_id=update.message.chat_id)

    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("Список новых заявок")],
         [KeyboardButton("Мои заявки")], ],
        resize_keyboard=True
    )
    update.message.reply_text(text=message, reply_markup=reply_markup)

def show_subcontractor_order_keyboard(update, context):

    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("Вопрос заказчику")],
         [KeyboardButton("Изменить статус заявки")],
         [KeyboardButton("Назад")], ],
        resize_keyboard=True
    )
    update.message.reply_text(text='Выберите дальнейшее действие', reply_markup=reply_markup)

def show_client_order_keyboard(update, context):
    message = f'Список Ваших заявок. Выберите дальнейшее действие'

    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("Внести изменение в заявку")],
         [KeyboardButton("Назад")], ],
        resize_keyboard=True
    )
    update.message.reply_text(text=message, reply_markup=reply_markup)

def show_status_order_keyboard(update, context):
    message = 'Выберите новый статус заявки'
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("Выполнен")],
         [KeyboardButton("Отклонен")],
         [KeyboardButton("Назад")], ],
        resize_keyboard=True
    )
    update.message.reply_text(text=message, reply_markup=reply_markup)

def get_client_orders(update, orders):
    if not orders:
        update.message.reply_text('Заявок нет')
        return 'CLIENT_MENU'

    message = ''
    for order in orders:
        message += f'''
                Номер заявки: {order.id}
                Описание заявки: {order.description}
                Подрядчик: {order.subcontractor}
                Статус заявки: {order.status}
                ____________________________________
            '''
    update.message.reply_text(message)

def get_subcontractor_orders(update, orders):
    if not orders:
        update.message.reply_text('Новых заявок нет')
        return 'SUBCONTRACTOR_MENU'

    message = ''
    for order in orders:
        message += f'''
                Номер заявки: {order.id}
                Описание заявки: {order.description}
                Логин от админки: {order.client_site_login}
                Пароль от админки: {order.client_site_password}
                Клиент: {order.client}
                ____________________________________
            '''
    update.message.reply_text(message)

def get_current_subscription(client):
    current_month = datetime.date.today().month
    return Subscription.objects.filter(client=client,
                                       begins_at__month=current_month)
