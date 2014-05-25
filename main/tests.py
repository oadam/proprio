from unittest import TestCase
from models import sum_payments, sum_fees, revision_to_fees,\
    revisions_to_fees, Tenant, RentRevision, Payment, Fee
from datetime import date


class TenantBalanceTests(TestCase):

    def test_fees(self):
        fee = Fee(date=date(2011, 3, 15), amount=300.12)
        "fees are counted as negative"
        self.assertEqual(-300.12, sum_fees(date(2011, 4, 1), [fee]))
        "fees are counted only after next month has begun"
        self.assertEqual(0, sum_fees(date(2011, 3, 22), [fee]))

    def test_payments(self):
        payment = Payment(amount=100, date=date(2011, 6, 15))
        "payments are counted as positive"
        self.assertEqual(100, sum_payments(date(2011, 6, 15), [payment]))
        "payments are counted only after current date"
        self.assertEqual(0, sum_payments(date(2011, 6, 14), [payment]))

    def test_revision_to_fees(self):
        revision = RentRevision(
            date=date(2011, 4, 1),
            rent=200,
            provision=100)
        "no fees before"
        self.assertSequenceEqual(
            [],
            revision_to_fees(revision, date(2010, 1, 1)))
        "first fee"
        self.assertSequenceEqual(
            [200, 100],
            [fee.amount for fee in revision_to_fees(
                revision,
                date(2011, 5, 1))])
        self.assertSequenceEqual(
            [date(2011, 5, 1), date(2011, 5, 1)],
            [fee.date for fee in revision_to_fees(revision, date(2011, 5, 1))])
        "following fees"
        self.assertEqual(6, len(revision_to_fees(revision, date(2011, 7, 1))))

    def test_revisions_to_fees(self):
        rentRevision1 = RentRevision(
            date=date(2011, 1, 1),
            rent=200,
            provision=100)
        rentRevision2 = RentRevision(
            date=date(2011, 3, 1),
            rent=300,
            provision=200)
        "no fees before"
        self.assertSequenceEqual([], revisions_to_fees(
            date(2010, 1, 1),
            [rentRevision1, rentRevision2],
            None))
        self.assertEqual(300, sum([f.amount for f in revisions_to_fees(
            date(2011, 2, 15),
            [rentRevision1, rentRevision2],
            None)]))
        self.assertEqual(1100, sum([f.amount for f in revisions_to_fees(
            date(2011, 4, 15),
            [rentRevision1, rentRevision2],
            None)]))
        self.assertEqual(1600, sum([f.amount for f in revisions_to_fees(
            date(2011, 8, 15),
            [rentRevision1, rentRevision2],
            date(2011, 5, 1))]))
