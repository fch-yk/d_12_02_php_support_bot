import time

import telegram
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import localtime

from tgbot.models import Order, Manager


class Command(BaseCommand):
    help = 'Starts the monitor bot'

    def handle(self, *args, **options):
        bot = telegram.Bot(token=settings.TELEGRAM_ACCESS_TOKEN)

        while True:
            now = localtime()
            orders = Order.objects.filter(
                status=Order.IN_PROGRESS,
                due_date__lt=now
            ).select_related('client', 'subcontractor')
            managers = Manager.objects.all()
            for order in orders:
                due_date = localtime(order.due_date)
                text = (
                    f'Заказ № {order.id} со сроком '
                    f'до {due_date.strftime("%d.%m.%Y %H:%M")} '
                    'не выполнен в срок'
                    f'\n Клиент: {order.client.name} '
                    f'({order.client.telegram_user_id})'
                    f'\n Подрядчик: {order.subcontractor.name} '
                    f'({order.subcontractor.telegram_user_id})'
                )
                for manager in managers:
                    bot.send_message(
                        chat_id=manager.telegram_user_id,
                        text=text
                    )
            time.sleep(settings.MONITOR_PAUSE)
