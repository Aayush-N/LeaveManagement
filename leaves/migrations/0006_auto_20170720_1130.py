# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0005_auto_20170720_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaves.LeaveType', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='leavetype',
            name='CL',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaves.EarnedLeave', verbose_name='CL'),
        ),
        migrations.AlterField(
            model_name='leavetype',
            name='EL',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaves.CasualLeave', verbose_name='EL'),
        ),
        migrations.AlterField(
            model_name='leavetype',
            name='ML',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaves.MaternityLeave', verbose_name='ML'),
        ),
        migrations.AlterField(
            model_name='leavetype',
            name='RH',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaves.RestrictedHoliday', verbose_name='RH'),
        ),
        migrations.AlterField(
            model_name='leavetype',
            name='SCL',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaves.SpecialCasualLeave', verbose_name='SCL'),
        ),
    ]
