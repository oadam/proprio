# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
            ],
            options={
                'verbose_name': 'building',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuildingFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('file', models.FileField(upload_to=b'building', verbose_name='file')),
                ('building', models.ForeignKey(verbose_name='building', to='main.Building')),
            ],
            options={
                'verbose_name': 'file',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('date', models.DateField(verbose_name='date')),
                ('amount', models.DecimalField(verbose_name='amount', max_digits=7, decimal_places=2)),
            ],
            options={
                'verbose_name': 'one-time fee',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1024, verbose_name='description', blank=True)),
                ('date', models.DateField(verbose_name='date')),
                ('amount', models.DecimalField(verbose_name='amount', max_digits=7, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'verbose_name': 'payment received from tenant',
                'verbose_name_plural': 'payments received from tenant',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('address', models.TextField(verbose_name='address')),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='building', blank=True, to='main.Building', null=True)),
            ],
            options={
                'verbose_name': 'property',
                'verbose_name_plural': 'properties',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PropertyFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('file', models.FileField(upload_to=b'property', verbose_name='file')),
                ('property', models.ForeignKey(verbose_name='property', to='main.Property')),
            ],
            options={
                'verbose_name': 'file',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RentRevision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(verbose_name='start date', validators=[main.models.validate_month])),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='end date', validators=[main.models.validate_month])),
                ('rent', models.DecimalField(verbose_name='monthly rent', max_digits=7, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('provision', models.DecimalField(verbose_name='monthly provision', max_digits=7, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'verbose_name': 'rent revision',
                'verbose_name_plural': 'rent revisions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('tenancy_begin_date', models.DateField(verbose_name='tenancy begin date')),
                ('tenancy_end_date', models.DateField(null=True, verbose_name='tenancy end date', blank=True)),
                ('deposit', models.DecimalField(default=0, verbose_name='deposit', max_digits=7, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('contact_info', models.TextField(verbose_name='contact info', blank=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='property', to='main.Property')),
            ],
            options={
                'verbose_name': 'tenant',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TenantFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('file', models.FileField(upload_to=b'tenant', verbose_name='file')),
                ('tenant', models.ForeignKey(verbose_name='tenant', to='main.Tenant')),
            ],
            options={
                'verbose_name': 'file',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rentrevision',
            name='tenant',
            field=models.ForeignKey(verbose_name='tenant', to='main.Tenant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='payment',
            name='tenant',
            field=models.ForeignKey(verbose_name='tenant', to='main.Tenant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fee',
            name='tenant',
            field=models.ForeignKey(verbose_name='tenant', to='main.Tenant'),
            preserve_default=True,
        ),
    ]
