# Generated by Django 3.1.6 on 2021-02-10 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wallets', '0011_auto_20210210_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction_history',
            name='trans_type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit'), ('fund_wallet', 'Fund Wallet')], max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='account_no',
            field=models.CharField(blank=True, default='7556565776', editable=False, max_length=10, unique=True),
        ),
    ]
