# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PublicHoliday',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('name', models.TextField(max_length=256)),
                ('type', models.TextField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
