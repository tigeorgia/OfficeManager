# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profileattachment',
            old_name='link',
            new_name='url',
        ),
        migrations.RemoveField(
            model_name='profileattachment',
            name='file',
        ),
    ]
