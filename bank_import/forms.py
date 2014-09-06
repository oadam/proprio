from django import forms
from django.forms.formsets import formset_factory
from importers import get_importers
from django.utils.translation import ugettext_lazy as _


def get_choices():
    importers = get_importers()
    choices = []
    for importer in importers:
        choices.append((importer.get_id(), importer.get_label(),))
    return choices


class UploadForm(forms.Form):
    type = forms.ChoiceField(choices=get_choices())
    file = forms.FileField()


class LineMappingForm(forms.Form):
    mapping = forms.ChoiceField(required=True, choices=[
        ('', _('Decide later')),
        (_('Automatic mapping'), (('{mapping:...}', 'Paiement edwige zaonne'),)),
        (_('Tenant payment'), (('{mapping:.....}', 'Olivier Adam'),('{mapping:.....}', 'Edwige Zaonne'),))
        ])

MappingForm = formset_factory(LineMappingForm, extra=0)
