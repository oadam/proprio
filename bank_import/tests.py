# vim: ai ts=4 sts=4 et sw=4
from django.test import TestCase
from views import create_formset
from main.models import Property, Tenant, Building
from datetime import date
from models import ImportLine
from django.contrib.auth.models import User
from django.test import Client


class BankImporter(TestCase):

    def setUp(self):
        building = Building.objects.create(name="test building")
        property = Property.objects.create(
            name="test property", building=building,
            address="test address")
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
            ImportLine(
                date=date(day=1, month=2, year=2011),
                amount=100,
                caption="Vir Olivier Adam rent february"),
            ]
        current_mapping = [{'mapping': ''} for x in lines]
        formset = create_formset(lines, current_mapping)
        choices = [form['mapping'].field.choices for form in formset]
        self.assertEquals(len(choices), 4)
        self.assertEquals([c[0][0] for c in choices], [''] * 4)
        self.assertEquals([c[1][0] for c in choices], ['HIDE'] * 4)
        # automatic guesses
        self.assertEquals([len(c[2][1]) for c in choices], [1, 1, 0, 1])
        a_choice = '["tenant_payment", {}]'.format(self.tenant_a.id)
        self.assertEquals(choices[0][2][1][0][0], a_choice)
        self.assertEquals(choices[3][2][1][0][0], a_choice)
        # exhaustive tenant choices
        self.assertEquals([len(c[3][1]) for c in choices], [2] * 4)

    def test_save(self):
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
        data = {
            'form-INITIAL_FORMS': '3',
            'form-TOTAL_FORMS': '3',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-mapping':
                '["tenant_payment", {}]'
                .format(self.tenant_a.id),
            'form-1-mapping':
                '["tenant_payment", {}]'
                .format(self.tenant_b.id),
            'form-2-mapping':
                '["tenant_payment", {}]'
                .format(self.tenant_b.id),
            #'form-2-mapping': ['HIDE']
        }
        current_mapping = [{'mapping': ''} for x in lines]
        formset = create_formset(lines, current_mapping, post=data)
        is_valid = formset.is_valid()
        self.assertTrue(is_valid)

    def test_upload_page(self):
        c = Client()
        c.login(username='toto', password='toto_pass')
        response = c.get('/import', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_submit(self):
        c = Client()
        c.login(username='toto', password='toto_pass')
        with open('bank_import/import_test.xlsx') as fp:
            response = c.post(
                '/import',
                {type: 'CIC-XLSX', file: fp},
                follow=True)
        self.assertEqual(response.status_code, 200)
