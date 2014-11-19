# vim: ai ts=4 sts=4 et sw=4
from unittest import TestCase
from views import create_formset
from main.models import Property, Tenant, Building
from datetime import date
from models import ImportLine


class BankImporter(TestCase):

    def test_guesses(self):
        building = Building.objects.create(name="test building")
        property = Property.objects.create(
            name="test property", building=building,
            address="test address")
        Tenant.objects.create(
            property=property, name="Olivier Adam",
            tenancy_begin_date=date(2011, 1, 1),
            tenancy_end_date=date(2013, 9, 1))
        Tenant.objects.create(
            property=property, name="John Doe",
            tenancy_begin_date=date(2011, 1, 1),
            tenancy_end_date=date(2013, 9, 1))
        lines = [
            ImportLine(
                date=date(day=1, month=1, year=2011),
                amount=100,
                caption="Vir Olivier Adam rent january"),
            ImportLine(
                date=date(day=3, month=1, year=2011),
                amount=600,
                caption="Doe rent"),
            ImportLine(
                date=date(day=3, month=1, year=2011),
                amount=12.98,
                caption="unrelated utility bill"),
            ]
        current_mapping = [{'mapping': ''} for x in lines]
        formset = create_formset(lines, current_mapping)
        choices = [form['mapping'].field.choices for form in formset]
        self.assertEquals(len(choices), 3)
        self.assertEquals([c[0][0] for c in choices], [''] * 3)
        self.assertEquals([c[1][0] for c in choices], ['HIDE'] * 3)
        # automatic guesses
        self.assertEquals([len(c[2][1]) for c in choices], [1, 1, 0])
        # exhaustive tenant choices
        self.assertEquals([len(c[3][1]) for c in choices], [2] * 3)
