# -*- coding: utf-8 -*-
from bank_import.models import ImportLine
from datetime import datetime
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
import os
import csv

# number of rows after which we give up searching for the header
GIVE_UP_AFTER = 30
HEADER = ('Date', 'Date valeur', 'Libell\xe9', 'D\xe9bit Euros', 'Cr\xe9dit Euros',)
STOP = (None, None, None, None, None,)


class _Importer:
    def get_label(self):
        return "CA - csv"

    def get_id(self):
        return "CA-CSV"

    def parse_row(self, row):
        date, date2, caption, debit, credit = row
        if debit == "" and credit == "":
            raise ValueError(
                u'both debit and credit are empty on line {}'.format(row))
        if debit != "" and credit != "":
            raise ValueError(
                u'both debit and credit are specified on line {}'.format(row))
        if debit != "":
            amount_string = "-" + debit
        if credit != "":
            amount_string = credit
        amount_string = amount_string.replace(',', '.')
        amount = Decimal(amount_string)
        amount = amount.quantize(Decimal('.01'))
        caption=unicode(caption,'windows-1252')
        date = datetime.strptime(date, '%d/%m/%Y').date()
        return ImportLine(date=date, caption=caption, amount=amount)

    def validate(self, file):
        filename, file_extension = os.path.splitext(file.name)
        if file_extension != '.CSV':
            return _(u'only CSV files are accepted for importer "{}"').format(self.get_id())
        else:
            return None

    def parse(self, file):
        rows = csv.reader(file, delimiter=";")
        result = []
        read_rows = 0
        header_found = False
        for row in rows:
            read_rows += 1
            if (len(row) < 5):
                values = STOP
            else:
                values = (
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],)
            if header_found:
                if values == STOP:
                    break
                result.append(self.parse_row(values))
            else:
                if values == HEADER:
                    header_found = True
                elif read_rows > GIVE_UP_AFTER:
                    raise ValueError(u'did not find row {}'.format(HEADER))
        return result


importer = _Importer()
