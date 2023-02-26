from django.conf import settings
from django.core.management import BaseCommand

from tgbot.tg_support import (
    TgSupportBot,
    start,
    handle_auth,
    handle_client_menu,
    handle_client_order_menu,
    handle_subcontractor_menu,
    handle_subcontractor_order_menu
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            start_bot()
        except Exception as exc:
            print(exc)


def start_bot():
    bot = TgSupportBot(
        settings.TELEGRAM_ACCESS_TOKEN,
        {
            'START': start,
            'HANDLE_AUTH': handle_auth,
            'CLIENT_MENU': handle_client_menu,
            'CLIENT_ORDER_MENU': handle_client_order_menu,
            'SUBCONTRACTOR_MENU': handle_subcontractor_menu,
            'SUBCONTRACTOR_ORDER_MENU': handle_subcontractor_order_menu,
        }
    )
    bot.updater.start_polling()
    bot.updater.idle()  # required in detached mode on server
