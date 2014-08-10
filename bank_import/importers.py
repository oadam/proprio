from django.conf import settings
from django.utils.module_loading import import_by_path

def get_importers():
    paths = settings.PROPRIO_IMPORT_PARSERS
    if settings == None:
        raise ValueError("PROPRIO_IMPORT_PARSERS django setting is required")
    result = []
    for path in paths:
        importer = import_by_path(path)
        result.append(importer)
    return result
