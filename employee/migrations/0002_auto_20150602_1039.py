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
            name='role',
            field=models.CharField(default=b'0-EMPL', max_length=64, choices=[(b'0-EMPL', b'Employee'), (b'2-OMAN', b'HR Manager'), (b'1-FMAN', b'Financial Manager')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='seniority',
            field=models.CharField(default=b'2-STD', max_length=64, choices=[(b'0-SEN', b'Senior Staff'), (b'1-MID', b'Middle Staff'), (b'2-STD', b'Staff'), (b'3-INT', b'Intern')]),
            preserve_default=True,
        ),
    ]
