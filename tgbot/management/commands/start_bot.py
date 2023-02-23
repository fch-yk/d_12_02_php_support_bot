from django.conf import settings
from django.core.management import BaseCommand

from tgbot.tg_support import TgSupportBot, handle_auth, start


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
        }
    )
    bot.updater.start_polling()
    bot.updater.idle()  # required in detached mode on server
