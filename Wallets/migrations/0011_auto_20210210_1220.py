# Generated by Django 3.1.6 on 2021-02-10 12:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Wallets', '0010_auto_20210210_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wallet',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='account_no',
            field=models.CharField(blank=True, default='7593673415', editable=False, max_length=10, unique=True),
        ),
    ]