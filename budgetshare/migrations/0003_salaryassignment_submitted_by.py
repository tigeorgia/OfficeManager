# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_auto_20150603_1010'),
        ('budgetshare', '0002_delete_salarysourceimport'),
    ]

    operations = [
        migrations.AddField(
            model_name='salaryassignment',
            name='submitted_by',
            field=models.ForeignKey(related_name='submitted_id', default=1, to='employee.Profile'),
            preserve_default=False,
        ),
    ]
