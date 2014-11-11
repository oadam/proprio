from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms import UploadForm, MappingForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from main.models import Tenant
from from_settings import get_element
import json


IMPORTER_SETTINGS = 'PROPRIO_IMPORT_PARSERS'


@login_required
def upload(request):
    if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                    data = form.cleaned_data
                    importer = get_element(IMPORTER_SETTINGS, data['type'])
                    parsed_file = importer.parse(data['file'])
                    request.session['import_file'] = parsed_file
                    request.session['import_mapping'] = ['']*len(parsed_file)
                    mapping_url = reverse(mapping)
                    return HttpResponseRedirect(mapping_url)
    else:
            form = UploadForm()
    return render(request,  'bank_import/upload.html', {'form': form})


@login_required
def mapping(request):
    lines = request.session['import_file']
    if request.method == 'POST':
        formset = MappingForm(request.POST)
        if formset.is_valid():
            raise "TODO"
        else:
            # store formset_data
            cleaned = [f.cleaned_data.get('mapping') for f in formset]
            request.session['import_mapping'] = cleaned
    else:
        if request.session['import_mapping'] is None:
            return HttpResponseRedirect(reverse(upload))
        session_mapping = request.session['import_mapping']
        formset_data = [{'mapping': m} for m in session_mapping]
        formset = MappingForm(initial=formset_data)
        fill_formset(lines, formset)
    # formset is necessary for csrf protection
    context = {'zip': zip(lines, formset), 'formset': formset}
    return render(request, 'bank_import/mapping.html', context)


class TenantPaymentMapping:
    type = 'tenant_payment'
    caption = _('Tenant payment')

    def get_all_values(self):
        tenants = Tenant.objects.all().order_by('name')
        return [({'tenant_id': t.id}, t.name) for t in tenants]


mappings = (TenantPaymentMapping(),)


def fill_formset(lines, formset):
    """Computes the choices of the mapping formset"""
    for i in range(len(lines)):
        # hardcoded choices
        choices = [
            ('', _('Decide later')),
            ('HIDE', _('Hide line definitively')),
        ]
        # auto choices
        auto_mappings = []
        # TODO fill auto_mappings using guessers
        # guesser receives line and returns a list of (mapping, score,)
        # then all guesses are consolidated (score are summed)
        choices.append((_('Automatic mapping'), auto_mappings,))
        # all possible manual mappings
        for m in mappings:
            values = []
            for v in m.get_all_values():
                id = json.dumps((m.type, v[0],))
                caption = v[1]
                values.append((id, caption),)
            choices.append((m.caption, values,))
        formset[i].fields['mapping'].choices = choices
