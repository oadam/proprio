# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='area',
            field=models.DecimalField(default=0, verbose_name='surface area', max_digits=7, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='rooms',
            field=models.DecimalField(default=0, verbose_name='number of rooms', max_digits=2, decimal_places=0, validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=False,
        ),
    ]
