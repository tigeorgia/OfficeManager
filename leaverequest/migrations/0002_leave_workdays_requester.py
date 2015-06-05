# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaverequest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='workdays_requester',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
            preserve_default=False,
        ),
    ]
