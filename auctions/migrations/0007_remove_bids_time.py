# Generated by Django 3.0.8 on 2020-07-22 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200722_0430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='time',
        ),
    ]
