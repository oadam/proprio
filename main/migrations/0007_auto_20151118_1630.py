# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150217_2332'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='building',
            options={'ordering': ['name'], 'verbose_name': 'building', 'verbose_name_plural': 'buildings'},
        ),
        migrations.AlterModelOptions(
            name='fee',
            options={'ordering': ['-date'], 'verbose_name': 'one-time fee', 'verbose_name_plural': 'one-time fees'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-date'], 'verbose_name': 'payment received from tenant', 'verbose_name_plural': 'payments received from tenant'},
        ),
        migrations.AlterModelOptions(
            name='property',
            options={'ordering': ['name'], 'verbose_name': 'property', 'verbose_name_plural': 'properties'},
        ),
        migrations.AlterModelOptions(
            name='propertyfile',
            options={'verbose_name': 'file', 'verbose_name_plural': 'files'},
        ),
        migrations.AlterModelOptions(
            name='reminder',
            options={'ordering': ['-date'], 'verbose_name': 'reminder', 'verbose_name_plural': 'reminders'},
        ),
        migrations.AlterModelOptions(
            name='rentrevision',
            options={'ordering': ['-start_date'], 'verbose_name': 'rent revision', 'verbose_name_plural': 'rent revisions'},
        ),
        migrations.AlterModelOptions(
            name='tenant',
            options={'ordering': ['name'], 'verbose_name': 'tenant', 'verbose_name_plural': 'tenants'},
        ),
        migrations.AlterModelOptions(
            name='tenantfile',
            options={'verbose_name': 'file', 'verbose_name_plural': 'files'},
        ),
    ]
