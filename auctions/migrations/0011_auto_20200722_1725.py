# Generated by Django 3.0.8 on 2020-07-22 17:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20200722_0648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watcher',
            field=models.ManyToManyField(blank=True, related_name='watcher', to=settings.AUTH_USER_MODEL),
        ),
    ]
