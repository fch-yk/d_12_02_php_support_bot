import textwrap

from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from telegram.ext import Filters, Updater

from .models import ChatState, RegistrationRequest, Client, Subcontractor
from .tg_lib import show_auth_keyboard, show_client_menu_keyboard


def start(update, context):
    chat_id = update.message.chat_id
    is_client = Client.objects.filter(telegram_user_id=chat_id)
    subcontractor_id = Subcontractor.objects.filter(telegram_user_id=chat_id)

    if is_client:
        client_name = is_client.first().name
        show_client_menu_keyboard(update, context, client_name)
        return "CLIENT_MENU"

    if not (is_client and subcontractor_id):
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
    if 'Список' in update.message.text:
        update.message.reply_text('Список заявок')
    else:
        update.message.reply_text('Новая заявка')
    return 'CLIENT_MENU'

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
