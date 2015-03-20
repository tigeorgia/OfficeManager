# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSheetManager', '0007_auto_20150319_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='leaves',
        ),
    ]
