# Generated by Django 3.0.8 on 2020-07-22 06:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200722_0521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='user',
        ),
        migrations.AddField(
            model_name='listing',
            name='watcher',
            field=models.ManyToManyField(blank=True, null=True, related_name='watcher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('HM', 'Home'), ('FS', 'Fashion'), ('TY', 'Toys'), ('EL', 'electronics'), ('OT', 'Other')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='picture',
            field=models.URLField(blank=True, null=True),
        ),
    ]
