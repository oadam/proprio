from django import forms
from importers import get_importers


def get_choices():
    importers = get_importers()
    choices = []
    for importer in importers:
        choices.append((importer.get_id(), importer.get_label(),))
    return choices


class UploadForm(forms.Form):
    type = forms.ChoiceField(choices=get_choices())
    file = forms.FileField()
