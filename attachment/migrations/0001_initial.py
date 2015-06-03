# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(max_length=512)),
                ('link', models.TextField(max_length=1024)),
                ('file', models.FileField(max_length=512, upload_to=b'attachments')),
                ('profile', models.ForeignKey(to='employee.Profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
