# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSheetManager', '0004_auto_20150318_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='leave_balance_HOLS',
            field=models.DecimalField(max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='leave_balance_SICK',
            field=models.DecimalField(max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='leave_earn_HOLS',
            field=models.DecimalField(max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='leave_earn_SICK',
            field=models.DecimalField(max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='leave_used_HOLS',
            field=models.DecimalField(max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='leave_used_SICK',
            field=models.DecimalField(max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
    ]
