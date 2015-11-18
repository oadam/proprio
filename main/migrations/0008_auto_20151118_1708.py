# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20151118_1630'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tenant',
            options={'ordering': ['tenancy_end_date', 'name'], 'verbose_name': 'tenant', 'verbose_name_plural': 'tenants'},
        ),
    ]
