# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datetime import date, timedelta
from main.models import next_month
from random import randrange
from django.contrib.auth.models import User
from django.conf import settings


def create_demo_data(apps, schema_editor):
    if settings.TESTING:
        return
    # only run for demos
    if User.objects.count() != 0:
        print("demo context skipped")
        return
    User.objects.create_superuser(
        username='demo', email='demo@gmail.com', password='demo')

    Building = apps.get_model("main", "Building")
    Property = apps.get_model("main", "Property")
    Tenant = apps.get_model("main", "Tenant")
    RentRevision = apps.get_model("main", "RentRevision")
    # Fee = apps.get_model("main", "Fee")
    Payment = apps.get_model("main", "Payment")

    building = Building.objects.create(name="Immeuble Paris")
    property1 = Property.objects.create(
        name="Appartement 1", building=building,
        address="23 rue de la maréchaussée", area=103, rooms=4)
    tenant1 = Tenant.objects.create(
        property=property1, name="Paul Bismuth",
        tenancy_begin_date=next_month(date.today(), -5))
    rent1 = RentRevision.objects.create(
        tenant=tenant1, start_date=tenant1.tenancy_begin_date,
        rent=1700, provision=100)
    # he payed ok until last month
    for i in range(-5, -1):
        late_days = randrange(20)
        d = next_month(date.today(), i) + timedelta(days=late_days)
        Payment.objects.create(
            tenant=tenant1, date=d,
            amount=rent1.rent + rent1.provision, description="bank transfer")
    # and only payed part of the money last month
    late_days = randrange(20)
    d = next_month(date.today(), -1) + timedelta(days=late_days)
    Payment.objects.create(
        tenant=tenant1, date=d, amount=rent1.rent * 3 / 4,
        description="sorry this is not much :-(")


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150208_1831'),
    ]

    operations = [
        migrations.RunPython(create_demo_data),
    ]
