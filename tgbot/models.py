from django.db import models


class RegistrationRequest(models.Model):
    CLIENT = 'CLI'
    SUBCONTRACTOR = 'SUB'
    ROLE_CHOICES = [
        (CLIENT, 'Клиент'),
        (SUBCONTRACTOR, 'Подрядчик'),
    ]

    UNPROCESSED = '1-UP'
    COMPLETED = '2-CO'
    DECLINED = '3-DE'
    STATUS_CHOICES = [
        (UNPROCESSED, 'Необработанный'),
        (COMPLETED, 'Выполнен'),
        (DECLINED, 'Отклонен'),
    ]

    partner_role = models.CharField(
        verbose_name='роль партнера',
        max_length=3,
        choices=ROLE_CHOICES,
        db_index=True,
    )

    name = models.CharField(
        verbose_name='наименование',
        max_length=150,
    )

    description = models.TextField(
        verbose_name='описание',
    )

    status = models.CharField(
        verbose_name='Статус',
        max_length=4,
        choices=STATUS_CHOICES,
        default=UNPROCESSED,
        db_index=True,
    )

    created_at = models.DateTimeField(
        verbose_name='создан в',
        auto_now_add=True,
        db_index=True,
    )

    modified_at = models.DateTimeField(
        verbose_name='изменен в',
        auto_now=True,
        db_index=True,
    )

    telegram_user_id = models.IntegerField(
        verbose_name='ID пользователя Telegram',
    )

    class Meta:
        verbose_name = 'запрос на регистрацию'
        verbose_name_plural = 'запросы на регистрацию'
        ordering = ['status', 'created_at']

    def __str__(self):
        return (
            f'Запрос на регистрацию № {self.id} '
            f'{self.get_partner_role_display()} {self.name}'
        )


class ChatState(models.Model):

    chat_id = models.IntegerField(
        'идентификатор чата',
        primary_key=True,
    )
    state = models.CharField(
        'состояние',
        max_length=100,
    )

    created_at = models.DateTimeField(
        verbose_name='создан в',
        auto_now_add=True,
        db_index=True,
    )

    modified_at = models.DateTimeField(
        verbose_name='изменен в',
        auto_now=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'состояние чата'
        verbose_name_plural = 'состояния чатов'
        ordering = ['-modified_at']

    def __str__(self):
        return f'Состояние чата {self.chat_id}'


class Partner(models.Model):
    telegram_user_id = models.IntegerField(
        verbose_name='ID пользователя Telegram',
        primary_key=True,
    )
    name = models.CharField(
        verbose_name='наименование',
        max_length=150,
        db_index=True,
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return (
            f'{self._meta.verbose_name.capitalize()} {self.name} '
            f'({self.telegram_user_id})'
        )


class Client(Partner):
    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Subcontractor(Partner):
    is_banned = models.BooleanField(
        verbose_name='заблокирован',
        db_index=True,
        default=False,
    )

    class Meta:
        verbose_name = 'подрядчик'
        verbose_name_plural = 'подрядчики'


class Manager(Partner):
    class Meta:
        verbose_name = 'менеджер'
        verbose_name_plural = 'менеджеры'
