# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImportedLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='date')),
                ('amount', models.DecimalField(verbose_name='amount', max_digits=7, decimal_places=2)),
                ('caption', models.CharField(max_length=1024, verbose_name='caption')),
                ('mapping', models.CharField(max_length=1024, verbose_name='mapping')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
