from bank_import.models import ImportLine
from datetime import date


class _Importer:
    def get_label(self):
        return "CIC - xlsx"

    def get_id(self):
        return "CIC-XLSX"

    def parse(self, file):
        return [
            ImportLine(
                date=date(day=1, month=1, year=2011),
                amount=100,
                caption="Vir Ewige Zaone loyer janvier"),
            ImportLine(
                date=date(day=3, month=2, year=2011),
                amount=100,
                caption="Vir Ewige Zaone loyer fevrier"),
            ]

importer = _Importer()
