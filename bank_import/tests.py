# vim: ai ts=4 sts=4 et sw=4
from django.test import TestCase
from views import (
    guess, submit_lines, remove_saved_lines, get_mappers_and_guessers,)
from main.models import Property, Tenant, Building, Payment
from datetime import date
from models import ImportLine, ImportedLine
from django.contrib.auth.models import User
from django.test import Client
from decimal import Decimal
import views


class BankImporter(TestCase):
    @classmethod
    def setUpClass(cls):
        # MIN_SCORE has been optimized based on the number of tenants
        # since we only have 2 tenants we'll never match anything with
        # a non-zero min_score
        cls.prevMinScore = views.MIN_SCORE
        views.MIN_SCORE = 0.0

    @classmethod
    def tearDownClass(cls):
        views.MIN_SCORE = cls.prevMinScore

    def setUp(self):
        building = Building.objects.create(name="test building")
        property = Property.objects.create(
            name="test property", building=building,
            address="test address", area=53, rooms=3)
        self.tenant_a = Tenant.objects.create(
            property=property, name="Olivier Adam",
            tenancy_begin_date=date(2011, 1, 1),
            tenancy_end_date=date(2013, 9, 1))
        self.tenant_b = Tenant.objects.create(
            property=property, name="John Doe",
            tenancy_begin_date=date(2011, 1, 1),
            tenancy_end_date=date(2013, 9, 1))
        User.objects.create_user(
            'toto', 'toto@gmail.com', 'toto_pass')

    def test_guesses(self):
        mappers, guessers = get_mappers_and_guessers()
        line1 = ImportLine(
            date=date(day=1, month=1, year=2011),
            amount=Decimal('100'),
            caption="Vir Olivier Adam rent january")
        expected1 = '["tenant_payment", {}]'.format(self.tenant_a.id)
        guess1, _ = guess(guessers, mappers, line1)
        self.assertEquals(guess1, expected1)
        line2 = ImportLine(
            date=date(day=3, month=1, year=2011),
            amount=Decimal('600'),
            caption="Doe rent")
        expected2 = '["tenant_payment", {}]'.format(self.tenant_b.id)
        guess2, _ = guess(guessers, mappers, line2)
        self.assertEquals(guess2, expected2)
        line3 = ImportLine(
            date=date(day=3, month=1, year=2011),
            amount=Decimal('12.98'),
            caption="unrelated utility bill")
        guess3 = guess(guessers, mappers, line3)
        self.assertEquals(guess3, None)

    def test_save(self):
        lines = [
            ImportedLine(
                date=date(day=1, month=1, year=2011),
                amount=Decimal('100'),
                caption="Vir Olivier Adam rent january",
                mapping='["tenant_payment", {}]'
                .format(self.tenant_a.id),),
            ImportedLine(
                date=date(day=3, month=1, year=2011),
                amount=Decimal('600'),
                caption="Doe rent",
                mapping='["tenant_payment", {}]'
                .format(self.tenant_a.id),),
            ImportedLine(
                date=date(day=3, month=1, year=2011),
                amount=Decimal('12.98'),
                caption="unrelated utility bill",
                mapping='HIDE',)
            ]
        submit_lines(lines)
        # we've mapped all lines so they should not reappear
        import_lines = [ImportLine(
            date=l.date,
            amount=l.amount,
            caption=l.caption)
            for l in lines]
        saved_removed = remove_saved_lines(import_lines)
        self.assertEqual(
            saved_removed, [],
            msg='imported lines stop showing up')
        # cashflows must have been created for tenants
        payments = Payment.objects.all()
        self.assertEqual(len(payments), 2)

    def test_upload_page(self):
        c = Client()
        c.login(username='toto', password='toto_pass')
        response = c.get('/import', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_generate(self):
        c = Client()
        c.login(username='toto', password='toto_pass')
        with open('bank_import/import_test.CSV') as fp:
            response = c.post(
                '/import/generate-mapping',
                {'type': 'CA-CSV', 'file': fp},
                follow=True)
        self.assertEqual(response.status_code, 200)

    def test_submit(self):
        c = Client()
        c.login(username='toto', password='toto_pass')
        with open('bank_import/submit_test.xlsx') as fp:
            response = c.post(
                '/import/submit-mapping',
                {'file': fp},
                follow=True)
        self.assertEqual(response.status_code, 200)
