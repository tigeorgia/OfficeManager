# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='leave_balance_before_HOLS',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timesheet',
            name='leave_balance_before_SICK',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
    ]
