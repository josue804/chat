# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-01 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20170326_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='lazy_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
