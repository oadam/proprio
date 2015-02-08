# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150208_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='description',
            field=models.CharField(max_length=1024, verbose_name='description'),
        ),
    ]
