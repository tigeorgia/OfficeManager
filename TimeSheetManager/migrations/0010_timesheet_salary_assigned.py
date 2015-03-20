# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSheetManager', '0009_remove_timesheet_salary_assigned'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='salary_assigned',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
