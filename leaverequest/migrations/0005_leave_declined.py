# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaverequest', '0004_auto_20150605_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='declined',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
