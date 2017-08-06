# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-21 14:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0023_auto_20170720_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='dep',
            field=models.CharField(default='CSE', max_length=3),
        ),
        migrations.AlterField(
            model_name='leavetaken',
            name='dateEnd',
            field=models.DateField(default=datetime.date(2017, 7, 21)),
        ),
        migrations.AlterField(
            model_name='leavetaken',
            name='dateStart',
            field=models.DateField(default=datetime.date(2017, 7, 21)),
        ),
        migrations.AlterField(
            model_name='leavetype',
            name='name',
            field=models.CharField(default='No name', max_length=120),
        ),
    ]
