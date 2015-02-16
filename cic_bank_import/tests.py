# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from django.test import TestCase
from datetime import date
from importer import importer
from bank_import.models import ImportLine
from decimal import Decimal


class ParseTest(TestCase):
    def test_parse(self):
        f = open('cic_bank_import/test-file.xlsm', 'rb')
        result = importer.parse(f)
        expected = [
            ImportLine(
                    date=date(day=1, month=12, year=2014),
                    amount=Decimal('100.25'),
                    caption="Libele 1"),
            ImportLine(
                    date=date(day=1, month=12, year=2014),
                    amount=Decimal('-1250'),
                    caption="Libele 2"),
            ImportLine(
                    date=date(day=2, month=12, year=2014),
                    amount=Decimal('550'),
                    caption=u"Libelé 3"),
            ]
        self.assertEquals(result, expected)
