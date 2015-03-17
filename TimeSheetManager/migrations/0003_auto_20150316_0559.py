# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSheetManager', '0002_auto_20150313_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salaryassignment',
            name='date',
        ),
        migrations.AddField(
            model_name='salaryassignment',
            name='period',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
