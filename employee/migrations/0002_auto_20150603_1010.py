# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(default=b'0-TBIL', max_length=64, choices=[(b'0-BATU', b'Batumi'), (b'0-TBIL', b'Tbilisi'), (b'0-ZUGD', b'Zugdidi'), (b'0-KUTA', b'Kutaisi')]),
            preserve_default=True,
        ),
    ]
