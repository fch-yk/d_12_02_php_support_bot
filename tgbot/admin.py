import telegram
from admin_extra_buttons.api import ExtraButtonsMixin, button
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.utils.timezone import localtime

from .models import (ChatState, Client, Manager, Order, RegistrationRequest,
                     Subcontractor, Subscription, Tariff)


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = [
        'telegram_user_id',
        'partner_role',
        'name',
        'status',
        'created_at',
    ]

    readonly_fields = ['id', 'created_at', 'modified_at']


@admin.register(ChatState)
class ChatStateAdmin(admin.ModelAdmin):
    list_display = [
        'chat_id',
        'state',
        'modified_at',
    ]
    readonly_fields = ['created_at', 'modified_at']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'telegram_user_id',
        'name',
    ]


@admin.register(Subcontractor)
class SubcontractorAdmin(admin.ModelAdmin):
    list_display = [
        'telegram_user_id',
        'name',
        'is_banned'
    ]
    list_editable = ['is_banned']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_banned:
            obj.orders.filter(
                status=Order.IN_PROGRESS,
            ).update(status=Order.UNPROCESSED)


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = [
        'telegram_user_id',
        'name',
    ]


@admin.register(Order)
class OrderAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = [
        'id',
        'client',
        'created_at',
        'due_date',
        'status',
        'subcontractor',
    ]
    readonly_fields = ['id', 'created_at', 'modified_at']
    ordering = ['status', 'created_at']

    @button(change_form=True, label='Напомнить менеджерам')
    def prompt_managers(self, request, id):
        response = ''
        bot = telegram.Bot(token=settings.TELEGRAM_ACCESS_TOKEN)
        order = Order.objects.get(id=id)
        created_at = localtime(order.created_at)
        managers = Manager.objects.all()
        for manager in managers:
            text = (
                'Разберитесь, почему долго не берут в работу '
                f'заказ № {order.id} '
                f'от {created_at.strftime("%d.%m.%Y %H:%M")}'
            )
            bot.send_message(chat_id=manager.telegram_user_id, text=text)
            response += (
                f'\n Отправлено сообщение менеджеру {manager.name} '
                f'с текстом "{text}"'
            )

        return HttpResponse(response)


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = [
        'variant',
        'max_orders_number',
        'fix_subcontractor_ability',
        'get_contractor_contacts_ability',
        'order_review_period',
    ]
    readonly_fields = ['id']
    ordering = ['variant']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'begins_at',
        'client',
        'tariff',
        'subcontractor',
    ]
    readonly_fields = ['id']
    ordering = ['begins_at']
