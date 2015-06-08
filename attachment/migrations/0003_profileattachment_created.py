# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachment', '0002_auto_20150604_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileattachment',
            name='created',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
