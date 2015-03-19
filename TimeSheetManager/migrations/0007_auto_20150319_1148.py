# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSheetManager', '0006_auto_20150319_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='leave_balance_HOLS',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='leave_balance_MATL',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='leave_balance_PATL',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='leave_balance_SICK',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='leave_balance_UNPD',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='leave_balance_HOLS',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='leave_balance_SICK',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='leave_earn_HOLS',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='leave_earn_SICK',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='leave_used_HOLS',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='leave_used_SICK',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
    ]
