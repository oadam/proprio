from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms import UploadForm, MappingForm
from django.http import HttpResponseRedirect
from importers import get_importer
from django.core.urlresolvers import reverse


@login_required
def upload(request):
    if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                    data = form.cleaned_data
                    importer = get_importer(data['type'])
                    parsed_file = importer.parse(data['file'])
                    request.session['import_file'] = parsed_file
                    request.session['import_mapping'] = [None]*len(parsed_file)
                    mapping_url = reverse(mapping)
                    return HttpResponseRedirect(mapping_url)
    else:
            form = UploadForm()
    return render(request,  'bank_import/upload.html', {'form': form})


@login_required
def mapping(request):
    if request.method == 'POST':
        formset = MappingForm(request.POST)
        if formset.is_valid():
            raise "TODO"
        else:
            #store formset
            request.session['import_mapping'] = [f.cleaned_data.get('mapping') for f in formset]
    else:
        if request.session['import_mapping'] is None:
            return HttpResponseRedirect(reverse(upload))
        formset_data = [{'mapping': m} for m in request.session['import_mapping']]
        formset = MappingForm(initial=formset_data)
    lines = request.session['import_file']
    context = {'zip': zip(lines, formset), 'formset': formset}
    return render(request, 'bank_import/mapping.html', context)
