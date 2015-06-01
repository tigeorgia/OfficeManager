# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.CharField(max_length=64)),
                ('salary_assigned', models.BooleanField(default=False)),
                ('submit_date', models.DateField()),
                ('approve_date', models.DateField(null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('approved_by', models.CharField(max_length=64)),
                ('leave_balance_HOLS', models.DecimalField(null=True, max_digits=4, decimal_places=2)),
                ('leave_balance_SICK', models.DecimalField(null=True, max_digits=4, decimal_places=2)),
                ('leave_earn_HOLS', models.DecimalField(null=True, max_digits=4, decimal_places=2)),
                ('leave_earn_SICK', models.DecimalField(null=True, max_digits=4, decimal_places=2)),
                ('leave_used_HOLS', models.DecimalField(null=True, max_digits=4, decimal_places=2)),
                ('leave_used_SICK', models.DecimalField(null=True, max_digits=4, decimal_places=2)),
                ('employee', models.ForeignKey(to='employee.Profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
