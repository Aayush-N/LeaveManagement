# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0008_auto_20170720_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavetype',
            name='CL',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='pizza'),
        ),
    ]
