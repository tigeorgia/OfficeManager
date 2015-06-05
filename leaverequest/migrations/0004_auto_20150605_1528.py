# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaverequest', '0003_auto_20150605_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='sick_balance',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leave',
            name='vacation_balance',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
            preserve_default=False,
        ),
    ]
