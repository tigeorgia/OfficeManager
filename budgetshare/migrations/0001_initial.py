# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalaryAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.CharField(max_length=64)),
                ('percentage', models.IntegerField()),
                ('employee', models.ForeignKey(to='employee.Profile')),
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
        migrations.AddField(
            model_name='salaryassignment',
            name='source',
            field=models.ForeignKey(to='budgetshare.SalarySource'),
            preserve_default=True,
        ),
    ]
