# Generated by Django 3.1.6 on 2021-02-09 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wallets', '0004_auto_20210209_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='account_no',
            field=models.CharField(blank=True, default='7583178480', editable=False, max_length=10, unique=True),
        ),
    ]
