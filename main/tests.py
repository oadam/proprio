# vim: ai ts=4 sts=4 et sw=4
from unittest import TestCase
from models import fees_to_cashflows, payments_to_cashflows, revision_to_cashflows,\
    revisions_to_cashflows, RentRevision, Payment,\
    Fee, Building, Property, Tenant
from django.contrib.auth.models import User
from datetime import date
from django.test import Client
from django.core import urlresolvers


class BasicIntegrationTest(TestCase):
    def setUp(self):
        self.building = Building.objects.create(name="test building")
        self.property = Property.objects.create(
            name="test property", building=self.building,
            address="test address")
        self.tenant = Tenant.objects.create(
            property=self.property, name="test tenant",
	    tenancy_begin_date=date(2011, 1, 1),
            tenancy_end_date=date(2013, 9, 1))
        self.rev1 = RentRevision.objects.create(
            tenant=self.tenant, start_date=date(2013, 1, 1),
	    end_date=date(2013, 4, 1),
	    rent=300, provision=100)
        self.rev2 = RentRevision.objects.create(
            tenant=self.tenant, start_date=date(2013, 4, 1),
	    rent=400, provision=200)
        self.fee = Fee.objects.create(
            tenant=self.tenant, description="test fee",
            date=date(2013, 3, 12), amount=0.03)
        self.payment = Payment.objects.create(
            tenant=self.tenant, date=date(2013, 12, 25), amount=4200.03)
        self.user = User.objects.create_user(
            'toto', 'toto@gmail.com', 'toto_pass')

    def tearDown(self):
        self.user.delete()
        self.payment.delete()
        self.fee.delete()
        self.rev2.delete()
        self.rev1.delete()
        self.tenant.delete()
        self.property.delete()
        self.building.delete()

    def test_root(self):
        c = Client()
        c.login(username='toto', password='toto_pass')
        response = c.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_tenants(self):
        c = Client()
        c.login(username='toto', password='toto_pass')
        reversed = urlresolvers.reverse('tenants')
        response = c.get(reversed)
        self.assertEqual(response.status_code, 200)

    def test_cashflows(self):
        c = Client()
        c.login(username='toto', password='toto_pass')
        reversed = urlresolvers.reverse(
            'tenant_cashflows', args=[self.tenant.id])
        response = c.get(reversed)
        self.assertEqual(response.status_code, 200)


def cashflow_to_tuple(cashflow):
    return (cashflow.date, cashflow.amount)


class TenantBalanceTests(TestCase):

    def test_fees(self):
        fee = Fee(date=date(2011, 3, 15), amount=300.12)
        expected = (fee.date, -fee.amount)
        self.assertEqual([expected], map(
            cashflow_to_tuple,
            fees_to_cashflows(date(2011, 3, 15), [fee])),
            "nominal")

        self.assertSequenceEqual(
            [],
            fees_to_cashflows(date(2011, 3, 14), [fee]),
            "fees are counted")

    def test_payments(self):
        payment = Payment(amount=100, date=date(2011, 6, 15))
        self.assertEqual([(payment.date, payment.amount)], map(
            cashflow_to_tuple,
            payments_to_cashflows(date(2011, 6, 15), [payment])),
            "payments are counted as positive")
        self.assertEqual(
            [],
            payments_to_cashflows(date(2011, 6, 14), [payment]),
            "payments are counted only after current date")

    def test_revision_to_fees(self):
        revision = RentRevision(
            start_date=date(2011, 4, 1),
            rent=200,
            provision=100)
        self.assertEqual(
            [],
            revision_to_cashflows(revision, date(2011, 4, 1)),
            "no fees before")
        self.assertEqual(
            [(date(2011, 4, 1), -200), (date(2011, 4, 1), -100)],
            map(cashflow_to_tuple, revision_to_cashflows(
                revision,
                date(2011, 5, 1))))
        self.assertEqual(
            6,
            len(revision_to_cashflows(revision, date(2011, 7, 1))),
            "following fees")

    def test_revisions_to_fees(self):
        rentRevision1 = RentRevision(
            start_date=date(2011, 1, 1),
	    end_date=date(2011, 3, 1),
            rent=200,
            provision=100)
        rentRevision2 = RentRevision(
            start_date=date(2011, 3, 1),
            end_date=date(2011, 5, 1),
            rent=300,
            provision=200)
        self.assertEqual(0, sum([f.amount for f in revisions_to_cashflows(
            date(1990, 1, 1),
            [rentRevision1, rentRevision2])]))
        self.assertEqual(-300, sum([f.amount for f in revisions_to_cashflows(
            date(2011, 1, 15),
            [rentRevision1, rentRevision2])]))
        self.assertEqual(-1100, sum([f.amount for f in revisions_to_cashflows(
            date(2011, 3, 15),
            [rentRevision1, rentRevision2])]))
        self.assertEqual(-1600, sum([f.amount for f in revisions_to_cashflows(
            date(2011, 8, 15),
            [rentRevision1, rentRevision2])]))
