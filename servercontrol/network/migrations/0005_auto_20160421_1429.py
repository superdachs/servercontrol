# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_interface_connection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interface',
            name='connection',
            field=models.CharField(default='ethernet', max_length=255),
        ),
    ]
