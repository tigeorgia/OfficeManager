# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_auto_20150611_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='workday_end',
            field=models.TimeField(default=datetime.time(18, 0)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='workday_start',
            field=models.TimeField(default=datetime.time(10, 0)),
        ),
    ]
