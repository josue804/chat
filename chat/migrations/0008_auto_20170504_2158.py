# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-05 04:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_customuser_subscriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='subscriptions',
            field=models.ManyToManyField(null=True, to='chat.Room'),
        ),
    ]
