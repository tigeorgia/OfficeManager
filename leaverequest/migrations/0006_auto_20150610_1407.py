# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaverequest', '0005_leave_declined'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='end_hour',
            field=models.TimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leave',
            name='start_hour',
            field=models.TimeField(null=True),
            preserve_default=True,
        ),
    ]
