# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_reminder_remindersbytenant'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RemindersByTenant',
        ),
        migrations.CreateModel(
            name='TenantReminders',
            fields=[
            ],
            options={
                'verbose_name': 'tenant reminder list',
                'proxy': True,
                'verbose_name_plural': 'tenants reminder lists',
            },
            bases=('main.tenant',),
        ),
        migrations.AlterModelOptions(
            name='reminder',
            options={'verbose_name': 'reminder'},
        ),
    ]
