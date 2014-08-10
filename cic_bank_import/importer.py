'''private class'''
class _Importer:
    def get_label(self):
        return "CIC - xlsx"
    def get_id(self):
        return "CIC-XLSX"
    def parse(self, file):
        raise NotImplementedError("TODO")

importer = _Importer()
