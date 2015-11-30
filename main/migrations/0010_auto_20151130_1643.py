# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20151123_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('date', models.DateField(verbose_name='date')),
                ('amount', models.DecimalField(default=0, verbose_name='amount', max_digits=7, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'one-time discount',
                'verbose_name_plural': 'one-time discount',
            },
        ),
        migrations.AlterField(
            model_name='fee',
            name='amount',
            field=models.DecimalField(default=0, verbose_name='amount', max_digits=7, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='deposit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, validators=[django.core.validators.MinValueValidator(0)], help_text='A sum of money asked to tenant on day 1. It is payed back in full on the final day of the tenancy', verbose_name='deposit'),
        ),
        migrations.AddField(
            model_name='discount',
            name='tenant',
            field=models.ForeignKey(verbose_name='tenant', to='main.Tenant'),
        ),
    ]
