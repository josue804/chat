# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-26 23:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guestuser',
            name='ip_address',
        ),
        migrations.AddField(
            model_name='guestuser',
            name='session_key',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
