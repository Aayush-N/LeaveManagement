# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 12:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0012_leavetype_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavetype',
            name='CL',
            field=models.IntegerField(default=0, max_length=10),
        ),
    ]
