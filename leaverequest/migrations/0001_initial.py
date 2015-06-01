# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('type', models.CharField(default=b'HOLS', max_length=64, choices=[(b'UNPD', b'Unpaid Leave'), (b'OTHR', b'Other'), (b'MATL', b'M(P)aternity'), (b'HOLS', b'Vacation'), (b'SICK', b'Sick')])),
                ('comment', models.TextField(null=True, blank=True)),
                ('submit_date', models.DateField()),
                ('approve_date', models.DateField(null=True)),
                ('approved_by', models.CharField(max_length=64)),
                ('employee', models.ForeignKey(to='employee.Profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
