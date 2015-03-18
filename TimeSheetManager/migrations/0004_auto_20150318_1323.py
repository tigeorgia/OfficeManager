# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSheetManager', '0003_auto_20150316_0559'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='leave_balance_HOLS',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timesheet',
            name='leave_balance_SICK',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timesheet',
            name='leave_earn_HOLS',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timesheet',
            name='leave_earn_SICK',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timesheet',
            name='leave_used_HOLS',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timesheet',
            name='leave_used_SICK',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
