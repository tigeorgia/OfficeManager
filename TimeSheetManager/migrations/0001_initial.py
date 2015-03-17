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
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('workday_start', models.TimeField(default=b'10:00')),
                ('workday_end', models.TimeField(default=b'18:00')),
                ('break_hours', models.IntegerField(default=1)),
                ('location', models.CharField(max_length=64)),
                ('position', models.CharField(max_length=64)),
                ('role', models.CharField(default=b'EMPL', max_length=64, choices=[(b'EMPL', b'Employee'), (b'OMAN', b'Office Manager'), (b'FMAN', b'Financial Manager')])),
                ('leave_balance_HOLS', models.DecimalField(max_digits=4, decimal_places=2)),
                ('leave_balance_SICK', models.DecimalField(max_digits=4, decimal_places=2)),
                ('leave_balance_MATL', models.DecimalField(max_digits=4, decimal_places=2)),
                ('leave_balance_PATL', models.DecimalField(max_digits=4, decimal_places=2)),
                ('leave_balance_UNPD', models.DecimalField(max_digits=4, decimal_places=2)),
                ('leave_earn_HOLS', models.DecimalField(default=2.0, max_digits=4, decimal_places=2)),
                ('leave_earn_SICK', models.DecimalField(default=1.08, max_digits=4, decimal_places=2)),
                ('supervisor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(related_name='id_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
                ('employee', models.ForeignKey(to='TimeSheetManager.Employee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SalaryAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('percentage', models.IntegerField()),
                ('employee', models.ForeignKey(to='TimeSheetManager.Employee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SalarySource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
                ('employee', models.ForeignKey(to='TimeSheetManager.Employee')),
                ('leaves', models.ManyToManyField(to='TimeSheetManager.Leave')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='salaryassignment',
            name='source',
            field=models.ForeignKey(to='TimeSheetManager.SalarySource'),
            preserve_default=True,
        ),
    ]
