# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-27 10:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0024_auto_20170721_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavetaken',
            name='approval',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='leavetaken',
            name='dateEnd',
            field=models.DateField(default=datetime.date(2017, 7, 27)),
        ),
        migrations.AlterField(
            model_name='leavetaken',
            name='dateStart',
            field=models.DateField(default=datetime.date(2017, 7, 27)),
        ),
    ]
