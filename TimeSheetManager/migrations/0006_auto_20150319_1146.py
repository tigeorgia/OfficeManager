# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSheetManager', '0005_auto_20150319_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='leave_balance_HOLS',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employee',
            name='leave_balance_MATL',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employee',
            name='leave_balance_PATL',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employee',
            name='leave_balance_SICK',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employee',
            name='leave_balance_UNPD',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
    ]
