# Generated by Django 3.0.3 on 2020-03-09 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramuser',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='last_login',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
