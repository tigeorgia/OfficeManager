# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSheetManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='approved_by',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timesheet',
            name='approved_by',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
