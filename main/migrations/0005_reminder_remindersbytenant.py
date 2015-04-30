# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_demodata_20150215_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='date')),
                ('text', models.TextField(verbose_name='description')),
                ('read', models.BooleanField(default=False, verbose_name='mark as read')),
                ('tenant', models.ForeignKey(verbose_name='tenant', to='main.Tenant')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RemindersByTenant',
            fields=[
            ],
            options={
                'verbose_name': 'reminders by tenant',
                'proxy': True,
            },
            bases=('main.tenant',),
        ),
    ]
