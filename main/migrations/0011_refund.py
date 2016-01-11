# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20151130_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1024, verbose_name='description')),
                ('date', models.DateField(verbose_name='date')),
                ('amount', models.DecimalField(verbose_name='amount', max_digits=7, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('tenant', models.ForeignKey(verbose_name='tenant', to='main.Tenant')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'money transfer to tenant',
                'verbose_name_plural': 'money transfers to tenant',
            },
        ),
    ]
