# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-05 06:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_auto_20170504_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, to='chat.Room'),
        ),
    ]
