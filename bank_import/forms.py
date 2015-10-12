from django import forms
from from_settings import get_elements, get_element

IMPORTER_SETTINGS = 'PROPRIO_IMPORT_PARSERS'


def get_choices():
    importers = get_elements(IMPORTER_SETTINGS)
    choices = []
    for importer in importers:
        choices.append((importer.get_id(), importer.get_label(),))
    return choices


class GenerateForm(forms.Form):
    type = forms.ChoiceField(choices=get_choices())
    file = forms.FileField()

    def clean(self):
        cleaned_data = super(GenerateForm, self).clean()
        type = cleaned_data.get("type")
        file = cleaned_data.get("file")
        importer = get_element(IMPORTER_SETTINGS, type)
        error = importer.validate(file)
        if error is not None:
            raise forms.ValidationError(error)


class SubmitForm(forms.Form):
    file = forms.FileField()
