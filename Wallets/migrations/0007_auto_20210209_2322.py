# Generated by Django 3.1.6 on 2021-02-09 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wallets', '0006_auto_20210209_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='account_no',
            field=models.CharField(blank=True, default='7507510919', editable=False, max_length=10, unique=True),
        ),
    ]
