# Generated by Django 3.0.2 on 2020-01-09 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensetransaction',
            name='tags',
            field=models.CharField(blank=True, default='', max_length=4096, null=True, verbose_name='Comma separated transaction tags'),
        ),
    ]
