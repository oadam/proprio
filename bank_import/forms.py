from django import forms
from django.forms.formsets import formset_factory
from from_settings import get_elements

IMPORTER_SETTINGS = 'PROPRIO_IMPORT_PARSERS'


def get_choices():
    importers = get_elements(IMPORTER_SETTINGS)
    choices = []
    for importer in importers:
        choices.append((importer.get_id(), importer.get_label(),))
    return choices


class UploadForm(forms.Form):
    type = forms.ChoiceField(choices=get_choices())
    file = forms.FileField()


class LineMappingForm(forms.Form):
    mapping = forms.ChoiceField(required=False)


MappingForm = formset_factory(LineMappingForm, extra=0)
