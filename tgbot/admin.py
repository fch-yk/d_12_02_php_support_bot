from django.contrib import admin

from .models import (ChatState, Client, Manager, Order, RegistrationRequest,
                     Subcontractor)


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


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = [
        'telegram_user_id',
        'name',
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
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
