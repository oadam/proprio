from django.conf import settings
from django.utils.module_loading import import_by_path


def get_importers():
    paths = settings.PROPRIO_IMPORT_PARSERS
    if settings is None:
        raise ValueError("PROPRIO_IMPORT_PARSERS django setting is required")
    result = []
    for path in paths:
        importer = import_by_path(path)
        result.append(importer)
    return result


def get_importer(id):
    importers = get_importers()
    filtered = [i for i in importers if i.get_id() == id]
    assert len(filtered) == 1
    return filtered[0]
