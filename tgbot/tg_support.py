from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from telegram.ext import Filters, Updater

from .tg_lib import show_auth_keyboard, show_registration_keyboard

from .models import ChatState

def start(update, context):
    show_auth_keyboard(update, context)
    return "HANDLE_AUTH"


def handle_auth(update, context):
    show_registration_keyboard(update, context)
    return 'HANDLE_NEW_USER'


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

        chat_state,_ = ChatState.objects.get_or_create(chat_id=chat_id)

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
