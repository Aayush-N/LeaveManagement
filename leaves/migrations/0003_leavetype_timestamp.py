# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0002_auto_20170720_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavetype',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
