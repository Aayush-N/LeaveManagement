# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0011_auto_20170720_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavetype',
            name='name',
            field=models.CharField(default='No name', max_length=120),
        ),
    ]
