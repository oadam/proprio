from django.conf import settings
from django.utils.module_loading import import_string

# This utility get elements from the django config file
# The objective is to have extension points at runtime
# for example to register new bank file parsers


def get_elements(property_name):
    paths = getattr(settings, property_name)
    if paths is None:
        raise ValueError("{} django setting is required".format(property_name))
    result = []
    for path in paths:
        result.append(import_string(path))
    return result


def get_element(property_name, id):
    elements = get_elements(property_name)
    filtered = [i for i in elements if i.get_id() == id]
    assert len(filtered) == 1
    return filtered[0]
