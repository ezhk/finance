# Generated by Django 3.0.2 on 2020-01-05 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=2048, verbose_name='Asset category description')),
                ('balance', models.DecimalField(decimal_places=4, default=0, max_digits=19, verbose_name='Current money balance')),
                ('kind', models.CharField(blank=True, choices=[('CA', 'Cash'), ('BC', 'Bank card'), ('CC', 'Credit card')], max_length=2, verbose_name='Kind of asset')),
                ('image', models.ImageField(blank=True, upload_to='asset-images', verbose_name='Asset image preview')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=2048, verbose_name='Expense category description')),
                ('monthly_limit', models.FloatField(default=None, null=True, verbose_name='Monthly expenses limit')),
                ('image', models.ImageField(blank=True, upload_to='expense-images', verbose_name='Expense image preview')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=2048, verbose_name='Income source description')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('amount', models.DecimalField(decimal_places=4, default=0, max_digits=19, verbose_name='Income maney amount')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Asset')),
                ('income', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.IncomeSource')),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('amount', models.DecimalField(decimal_places=4, default=0, max_digits=19, verbose_name='Expense maney amount')),
                ('tags', models.CharField(blank=True, default=None, max_length=4096, null=True, verbose_name='Comma separated transaction tags')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Asset')),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ExpenseCategory')),
            ],
        ),
    ]