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
                ('role', models.CharField(default=b'0-EMPL', max_length=64, choices=[(b'0-EMPL', b'Employee'), (b'2-OMAN', b'HR Manager'), (b'1-FMAN', b'Financial Manager')])),
                ('seniority', models.CharField(default=b'2-STD', max_length=64, choices=[(b'0-SEN', b'Senior Staff'), (b'1-MID', b'Middle Staff'), (b'2-STD', b'Staff'), (b'3-INT', b'Intern')])),
                ('picture', models.ImageField(null=True, upload_to=b'profile')),
                ('mobile_num', models.CharField(max_length=256, null=True)),
                ('personal_num', models.CharField(max_length=256, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('address', models.TextField(null=True)),
                ('employment_status', models.CharField(default=b'0-FULL', max_length=64, null=True, choices=[(b'1-PART', b'Part time'), (b'0-FULL', b'Full time')])),
                ('contract_start', models.DateField(null=True)),
                ('contract_end', models.DateField(null=True)),
                ('salary_gross_usd', models.DecimalField(null=True, max_digits=16, decimal_places=2)),
                ('salary_net_usd', models.DecimalField(null=True, max_digits=16, decimal_places=2)),
                ('insurance', models.BooleanField(default=False)),
                ('gsm_limit', models.DecimalField(default=b'0.0', max_digits=16, decimal_places=2)),
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
