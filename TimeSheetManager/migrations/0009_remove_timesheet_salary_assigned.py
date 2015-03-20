# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSheetManager', '0008_remove_timesheet_leaves'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='salary_assigned',
        ),
    ]
