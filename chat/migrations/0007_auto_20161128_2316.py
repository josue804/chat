# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 07:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_guestuser_ip_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guestuser',
            old_name='name',
            new_name='username',
        ),
    ]