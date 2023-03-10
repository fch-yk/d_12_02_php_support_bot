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


class Order(models.Model):
    UNPROCESSED = 'A1-UP'
    IN_PROGRESS = 'B1-IP'
    COMPLETED = 'C1-CO'
    DECLINED = 'D1-DE'
    STATUS_CHOICES = [
        (UNPROCESSED, 'Необработанный'),
        (IN_PROGRESS, 'В работе'),
        (COMPLETED, 'Выполнен'),
        (DECLINED, 'Отклонен'),
    ]

    client = models.ForeignKey(
        'Client',
        on_delete=models.PROTECT,
        verbose_name='клиент',
        related_name='orders',
    )

    subcontractor = models.ForeignKey(
        'Subcontractor',
        on_delete=models.PROTECT,
        verbose_name='подрядчик',
        related_name='orders',
        blank=True,
        null=True,
    )

    description = models.TextField(
        verbose_name='описание',
    )

    time_estimation = models.TextField(
        verbose_name='оценка времени',
        blank=True,
    )

    status = models.CharField(
        verbose_name='статус',
        max_length=5,
        choices=STATUS_CHOICES,
        default=UNPROCESSED,
        db_index=True,
    )

    due_date = models.DateTimeField(
        verbose_name='срок',
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

    client_site_login = models.CharField(
        verbose_name='логин сайта клиента',
        max_length=20,
        blank=True,
        editable=False,
    )

    client_site_password = models.CharField(
        verbose_name='пароль сайта клиента',
        max_length=20,
        blank=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ № {self.id} от: {self.created_at} ({self.client})'


class Tariff(models.Model):
    ECONOMY = 'ECO'
    STANDARD = 'STA'
    VIP = 'VIP'
    VARIANT_CHOICES = [
        (ECONOMY, 'Эконом'),
        (STANDARD, 'Стандарт'),
        (VIP, 'VIP'),
    ]

    variant = models.CharField(
        verbose_name='вариант',
        max_length=3,
        choices=VARIANT_CHOICES,
        db_index=True,
    )
    max_orders_number = models.PositiveSmallIntegerField(
        verbose_name='максимальное количество заказов'
    )

    fix_subcontractor_ability = models.BooleanField(
        verbose_name='возможность закрепить подрядчика',
        default=False,
    )

    get_contractor_contacts_ability = models.BooleanField(
        verbose_name='возможность увидеть контакты подрядчика',
        default=False,
    )

    order_review_period = models.PositiveSmallIntegerField(
        verbose_name='срок рассмотрения заказа (в часах)'
    )

    class Meta:
        verbose_name = 'тариф'
        verbose_name_plural = 'тарифы'

    def __str__(self):
        return f'Тариф № {self.id} ({self.get_variant_display()})'


class Subscription(models.Model):
    begins_at = models.DateField(
        verbose_name='начинается с',

    )
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        verbose_name='клиент',
        related_name='subscriptions',
    )

    tariff = models.ForeignKey(
        'Tariff',
        on_delete=models.PROTECT,
        verbose_name='тариф',
        related_name='subscriptions',

    )

    subcontractor = models.ForeignKey(
        'Subcontractor',
        on_delete=models.PROTECT,
        verbose_name='подрядчик',
        related_name='subscriptions',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['begins_at', 'client'], name='unique_subscription'
            )
        ]

    def __str__(self):
        return f'Подписка {self.client}: {self.tariff} c {self.begins_at}'
