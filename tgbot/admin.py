from django.contrib import admin

from .models import RegistrationRequest, ChatState


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id',
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
