# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 12:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_interface_routes'),
    ]

    operations = [
        migrations.AddField(
            model_name='interface',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='interface',
            name='dhcp',
            field=models.BooleanField(default=False),
        ),
    ]
