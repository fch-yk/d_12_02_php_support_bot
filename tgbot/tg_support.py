import datetime
import textwrap

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from telegram.ext import Filters, Updater

from .models import ChatState, Client, Order, RegistrationRequest, Subcontractor, Manager
from .tg_lib import (get_client_orders, get_current_subscription, get_subcontractor_orders, show_auth_keyboard,
                     show_client_menu_keyboard, show_status_order_keyboard, show_subcontractor_menu_keyboard,
                     show_subcontractor_order_keyboard, show_client_order_keyboard)

from phpsupport.settings import ORDER_PRICE

def start(update, context):
    chat_id = update.message.chat_id
    is_client = Client.objects.filter(telegram_user_id=chat_id)
    is_subcontractor = Subcontractor.objects.filter(telegram_user_id=chat_id)

    if is_client:
        client_name = is_client.first().name
        update.message.reply_text(f'Здравствуйте {client_name}')

        if not get_current_subscription(is_client.first()):
            update.message.reply_text('У вас нет действующей подписки! Обратитесь к менеджеру')
            return "HANDLE_AUTH"

        show_client_menu_keyboard(update, context)
        return "CLIENT_MENU"

    if is_subcontractor:
        subcontractor = is_subcontractor.first()
        if subcontractor.is_banned:
            update.message.reply_text('Вам заблокирован доступ!')
            return "HANDLE_AUTH"
        show_subcontractor_menu_keyboard(update, context)
        return "SUBCONTRACTOR_MENU"

    if not (is_client and is_subcontractor):
        show_auth_keyboard(update, context)
        return "HANDLE_AUTH"


def handle_auth(update, context):
    if 'подрядчик' in update.message.text:
        context.user_data['partner_role'] = RegistrationRequest.SUBCONTRACTOR
    elif 'клиент' in update.message.text:
        context.user_data['partner_role'] = RegistrationRequest.CLIENT

    if '🔐' in update.message.text:
        update.message.reply_text('Введите свое имя и/или название организации')
        context.user_data['name'] = 'new'
        return "HANDLE_AUTH"
    elif context.user_data['name'] == 'new':
        context.user_data['name'] = update.message.text
        update.message.reply_text('Напишите коротко о себе и/или о вашей организации')
        context.user_data['description'] = 'new desc'
        return "HANDLE_AUTH"
    elif context.user_data['description'] == 'new desc':
        context.user_data['description'] = update.message.text
        RegistrationRequest.objects.create(
            name=context.user_data['name'],
            description=context.user_data['description'],
            partner_role=context.user_data['partner_role'],
            telegram_user_id=update.message.chat_id
        )

        message = textwrap.dedent('''
            Спасибо за вашу заявку
            В ближайшее время с вами свяжется наш менеджер!''')

        update.message.reply_text(text=message)
        return 'HANDLE_AUTH'


def handle_client_menu(update, context):
    user_data = context.user_data
    if 'Список' in update.message.text:
        client = Client.objects.get(telegram_user_id=update.message.chat_id)
        orders = Order.objects.filter(client=client)
        get_client_orders(update, orders)
        show_client_order_keyboard(update, context)
        return 'CLIENT_ORDER_MENU'

    if 'Помощь менеджера' in update.message.text:
        update.message.reply_text('Введите текст вопроса и нажмите Отправить',
                                  reply_markup=ReplyKeyboardRemove())
        user_data['client_menu'] = 'send_question'
        return 'CLIENT_MENU'
    elif user_data['client_menu'] == 'send_question':
        managers = Manager.objects.all()
        client = Client.objects.get(telegram_user_id=update.message.chat_id)
        for manager in managers:
            message = f'Вам сообщение от клиента {client.name}:'
            context.bot.send_message(chat_id=manager.telegram_user_id, text=message + update.message.text)
        update.message.reply_text('Сообщение успешно отправлено')
        return 'CLIENT_MENU'

    if 'Оформить' in update.message.text:
        update.message.reply_text('Введите описание вашей заявки', reply_markup=ReplyKeyboardRemove())
        user_data['order_detail'] = 'new_order_detail'

    elif user_data['order_detail'] == 'new_order_detail':
        user_data['order_detail'] = update.message.text
        update.message.reply_text('Введите срок выполнения (количество дней)')
        user_data['due'] = 'new_due'

    elif user_data['due'] == 'new_due':
        user_data['due'] = update.message.text
        update.message.reply_text('Введите логин для админ-панели сайта')
        user_data['site_login'] = 'new_site_login'

    elif user_data['site_login'] == 'new_site_login':
        user_data['site_login'] = update.message.text
        update.message.reply_text('Введите пароль для админ-панели сайта')
        user_data['site_password'] = 'new_site_password'

    elif user_data['site_password'] == 'new_site_password':
        user_data['site_password'] = update.message.text

        client = Client.objects.get(telegram_user_id=update.message.chat_id)
        order = Order.objects.create(
            client=client,
            description=user_data['order_detail'],
            due_date=datetime.date.today() + datetime.timedelta(days=int(user_data['due'])),
            client_site_login=user_data['site_login'],
            client_site_password=user_data['site_password']
        )

        message = textwrap.dedent(f'''
            Заявка {order.id} создана.
            В ближайшее время на нее будет назначен исполнитель!''')

        update.message.reply_text(text=message)
    return 'CLIENT_MENU'


def handle_client_order_menu(update, context):
    user_data = context.user_data
    if update.message.text == 'Назад':
        show_client_menu_keyboard(update, context)
        return "CLIENT_MENU"

    if 'Вопрос исполнителю' in update.message.text:
        update.message.reply_text('Выберите номер заявки по которой задать вопрос',
                                  reply_markup=ReplyKeyboardMarkup([['Назад']], resize_keyboard=True)
                                  )
        user_data['client_menu'] = 'change_order'
        return 'CLIENT_ORDER_MENU'

    elif user_data['client_menu'] == 'change_order':
        update.message.reply_text('Введите текст вопроса и нажмите Отправить',
                                  reply_markup=ReplyKeyboardRemove())
        user_data['order_id'] = int(update.message.text)
        user_data['client_menu'] = 'send_question'
        return 'CLIENT_ORDER_MENU'

    if user_data['client_menu'] == 'send_question':
        order = Order.objects.get(id=user_data['order_id'])
        subcontractor = order.subcontractor
        context.bot.send_message(chat_id=subcontractor.telegram_user_id, text=update.message.text)
        update.message.reply_text('Ваш вопрос успешно отправлен')
        show_client_menu_keyboard(update, context)
        return 'CLIENT_MENU'


def handle_subcontractor_menu(update, context):
    if update.message.text == 'Назад':
        show_subcontractor_menu_keyboard(update, context)
        return "SUBCONTRACTOR_MENU"

    if 'Список' in update.message.text:
        orders = Order.objects.filter(status=Order.UNPROCESSED)
        get_subcontractor_orders(update, orders)
        update.message.reply_text(f'Ставка за выполненный заказ составляет {ORDER_PRICE}')
        update.message.reply_text('Для выбора заявки выберите ее номер и нажмите Отправить',
                                  reply_markup=ReplyKeyboardMarkup([['Назад']], resize_keyboard=True)
                                  )

        context.user_data['subcontractor_menu'] = 'new_order'
    elif 'Мои' in update.message.text:
        subcontractor = Subcontractor.objects.get(telegram_user_id=update.message.chat_id)
        orders = Order.objects.filter(status=Order.IN_PROGRESS,
                                      subcontractor=subcontractor)
        get_subcontractor_orders(update, orders)
        show_subcontractor_order_keyboard(update, context)
        return 'SUBCONTRACTOR_ORDER_MENU'

    elif 'Финансы' in update.message.text:
        subcontractor = Subcontractor.objects.get(telegram_user_id=update.message.chat_id)
        complete_order_counts = Order.objects.filter(status=Order.COMPLETED,
                                                     subcontractor=subcontractor).count()
        message = f'''Всего выполнено заказов: {complete_order_counts}
                  Ставка за заказ: {ORDER_PRICE}
                  Заработано всего: {complete_order_counts*ORDER_PRICE}'''
        update.message.reply_text(text=message,
                                  reply_markup=ReplyKeyboardMarkup([['Назад']], resize_keyboard=True)
                                  )
        return 'SUBCONTRACTOR_ORDER_MENU'

    elif context.user_data['subcontractor_menu'] == 'new_order':
        subcontractor = Subcontractor.objects.get(telegram_user_id=update.message.chat_id)
        order = Order.objects.get(pk=update.message.text)

        order.subcontractor = subcontractor
        order.status = Order.IN_PROGRESS
        order.save()
        update.message.reply_text('Заявка сохранена за вами. Для ее просмотра перейдите в список ваших заявок')

    return 'SUBCONTRACTOR_MENU'


def send_question(update, context, user_data):
    client = Order.objects.get(id=user_data['order_id']).client
    context.bot.send_message(chat_id=client.telegram_user_id, text=update.message.text)

def handle_subcontractor_order_menu(update, context):
    user_data = context.user_data

    if update.message.text == 'Назад':
        show_subcontractor_menu_keyboard(update, context)
        return 'SUBCONTRACTOR_MENU'

    if 'Изменить статус заявки' in update.message.text:
        update.message.reply_text('Для смены статуса заявки выберите ее номер и нажмите Отправить',
                                  reply_markup=ReplyKeyboardMarkup([['Назад']], resize_keyboard=True)
                                  )
        user_data['order_menu'] = 'change_order'
        user_data['order_action'] = 'change_status'
        return 'SUBCONTRACTOR_ORDER_MENU'

    elif 'Вопрос заказчику' in update.message.text:
        update.message.reply_text('По какому заказу вопрос?',
                                  reply_markup=ReplyKeyboardMarkup([['Назад']], resize_keyboard=True)
                                  )
        user_data['order_menu'] = 'change_order'
        user_data['order_action'] = 'send_question'
        return 'SUBCONTRACTOR_ORDER_MENU'

    elif user_data['order_menu'] == 'change_order':
        user_data['order_id'] = int(update.message.text)

        if user_data['order_action'] == 'send_question':
            update.message.reply_text('Введите текст вопроса и нажмите Отправить',
                                      reply_markup=ReplyKeyboardRemove())
            user_data['order_menu'] = 'send_question'
        else:
            show_status_order_keyboard(update, context)
            user_data['order_menu'] = 'change_status'
        return 'SUBCONTRACTOR_ORDER_MENU'

    elif user_data['order_menu'] == 'send_question':
        send_question(update, context, user_data)
        update.message.reply_text('Сообщение успешно отправлено')
        show_subcontractor_menu_keyboard(update, context)
        return 'SUBCONTRACTOR_MENU'

    elif user_data['order_menu'] == 'change_status':
        status = update.message.text
        order_id = user_data['order_id']

        subcontractor = Subcontractor.objects.get(telegram_user_id=int(update.message.chat_id))
        order = subcontractor.orders.filter(id=order_id).first()
        if status == 'Выполнен':
            order.status = Order.COMPLETED
        elif status == 'Отклонен':
            order.status = Order.DECLINED
        order.save()

        update.message.reply_text('Статус заказа успешно изменен')
        show_subcontractor_menu_keyboard(update, context)

        message = f'Статус вашего заказа с №{order_id} изменен на {status}'
        context.bot.send_message(chat_id=order.client.telegram_user_id, text=message)

        return 'SUBCONTRACTOR_MENU'

class TgSupportBot(object):
    def __init__(self, tg_token, states_functions):
        self.tg_token = tg_token
        self.states_functions = states_functions
        self.updater = Updater(token=tg_token, use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler('start', self.handle_users_reply))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.handle_users_reply))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text | Filters.contact, self.handle_users_reply))

    def handle_users_reply(self, update, context):

        if update.message:
            user_reply = update.message.text
            chat_id = update.message.chat_id
        elif update.callback_query:
            user_reply = update.callback_query.data
            chat_id = update.callback_query.message.chat_id
        else:
            return

        chat_state, _ = ChatState.objects.get_or_create(chat_id=chat_id)

        if user_reply == '/start':
            user_state = 'START'
        else:
            user_state = chat_state.state

        state_handler = self.states_functions[user_state]
        try:
            next_state = state_handler(update, context)
            chat_state.state = next_state
            chat_state.save()
        except Exception as err:
            print(err)
