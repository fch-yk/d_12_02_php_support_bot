# Generated by Django 4.1.7 on 2023-02-23 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatState',
            fields=[
                ('chat_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='идентификатор чата')),
                ('state', models.CharField(max_length=100, verbose_name='состояние')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='создан в')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='изменен в')),
            ],
            options={
                'verbose_name': 'состояние чата',
                'verbose_name_plural': 'состояния чатов',
                'ordering': ['-modified_at'],
            },
        ),
        migrations.CreateModel(
            name='RegistrationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_role', models.CharField(choices=[('CLI', 'Клиент'), ('SUB', 'Подрядчик')], db_index=True, max_length=3, verbose_name='роль партнера')),
                ('name', models.CharField(max_length=150, verbose_name='наименование')),
                ('description', models.TextField(verbose_name='описание')),
                ('status', models.CharField(choices=[('1-UP', 'Необработанный'), ('2-CO', 'Выполнен'), ('3-DE', 'Отклонен')], db_index=True, default='1-UP', max_length=4, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='создан в')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='изменен в')),
            ],
            options={
                'verbose_name': 'запрос на регистрацию',
                'verbose_name_plural': 'запросы на регистрацию',
                'ordering': ['status', 'created_at'],
            },
        ),
    ]
