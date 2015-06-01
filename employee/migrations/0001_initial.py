# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.CharField(max_length=64)),
                ('location', models.CharField(max_length=64)),
                ('role', models.CharField(default=b'EMPL', max_length=64, choices=[(b'EMPL', b'Employee'), (b'OMAN', b'HR Manager'), (b'FMAN', b'Financial Manager')])),
                ('seniority', models.CharField(default=b'STD', max_length=64, choices=[(b'SEN', b'Senior Staff'), (b'INT', b'Intern'), (b'STD', b'Staff'), (b'MID', b'Middle Staff')])),
                ('workday_start', models.TimeField(default=b'10:00')),
                ('workday_end', models.TimeField(default=b'18:00')),
                ('leave_balance_HOLS', models.DecimalField(max_digits=4, decimal_places=2)),
                ('leave_balance_SICK', models.DecimalField(max_digits=4, decimal_places=2)),
                ('leave_balance_MATL', models.DecimalField(max_digits=4, decimal_places=2)),
                ('leave_balance_PATL', models.DecimalField(max_digits=4, decimal_places=2)),
                ('leave_balance_UNPD', models.DecimalField(max_digits=4, decimal_places=2)),
                ('leave_earn_HOLS', models.DecimalField(default=2.0, max_digits=4, decimal_places=2)),
                ('leave_earn_SICK', models.DecimalField(default=1.08, max_digits=4, decimal_places=2)),
                ('supervisor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(related_name='id_user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
