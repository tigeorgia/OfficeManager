# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaverequest', '0002_leave_workdays_requester'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leave',
            old_name='workdays_requester',
            new_name='workdays_requested',
        ),
    ]
