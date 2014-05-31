# vim: ai ts=4 sts=4 et sw=4
from unittest import TestCase
from models import fees_to_cashflows, payments_to_cashflows, revision_to_cashflows,\
    revisions_to_cashflows, RentRevision, Payment, Fee
from datetime import date
from django.test import Client


class BasicIntegrationTest(TestCase):

    def test(self):
        c = Client()
        c.get('/')


def cashflow_to_tuple(cashflow):
    return (cashflow.date, cashflow.amount)


class TenantBalanceTests(TestCase):

    def test_fees(self):
        fee = Fee(date=date(2011, 3, 15), amount=300.12)
        expected = (fee.date, -fee.amount)
        self.assertEqual([expected], map(
            cashflow_to_tuple,
            fees_to_cashflows(date(2011, 4, 1), [fee])), "nominal")

        self.assertSequenceEqual(
            [],
            fees_to_cashflows(date(2011, 3, 1), [fee]),
            "fees are counted only after next month has begun")

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
            date=date(2011, 4, 1),
            rent=200,
            provision=100)
        self.assertEqual(
            [],
            revision_to_cashflows(revision, date(2010, 1, 1)),
            "no fees before")
        self.assertEqual(
            [(date(2011, 5, 1), -200), (date(2011, 5, 1), -100)],
            map(cashflow_to_tuple, revision_to_cashflows(
                revision,
                date(2011, 5, 1))),
            "first fees")
        self.assertEqual(
            6,
            len(revision_to_cashflows(revision, date(2011, 7, 1))),
            "following fees")

    def test_revisions_to_fees(self):
        rentRevision1 = RentRevision(
            date=date(2011, 1, 1),
            rent=200,
            provision=100)
        rentRevision2 = RentRevision(
            date=date(2011, 3, 1),
            rent=300,
            provision=200)
        self.assertEqual([], revisions_to_cashflows(
            date(2010, 1, 1),
            [rentRevision1, rentRevision2],
            None))
        self.assertEqual(-300, sum([f.amount for f in revisions_to_cashflows(
            date(2011, 2, 15),
            [rentRevision1, rentRevision2],
            None)]))
        self.assertEqual(-1100, sum([f.amount for f in revisions_to_cashflows(
            date(2011, 4, 15),
            [rentRevision1, rentRevision2],
            None)]))
        self.assertEqual(-1600, sum([f.amount for f in revisions_to_cashflows(
            date(2011, 8, 15),
            [rentRevision1, rentRevision2],
            date(2011, 5, 1))]))
