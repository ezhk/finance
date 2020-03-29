# Generated by Django 3.0.4 on 2020-03-19 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_auto_20200309_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegrammessages',
            name='command',
        ),
        migrations.AddField(
            model_name='telegrammessages',
            name='json_message',
            field=models.CharField(blank=True, max_length=2048, verbose_name='User message presented as JSON'),
        ),
    ]
