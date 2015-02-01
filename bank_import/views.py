from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from forms import UploadForm, MappingForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from main.models import Tenant, Payment
from from_settings import get_element
from whoosh.filedb.filestore import RamStorage
from whoosh.fields import TEXT, NUMERIC, Schema
from whoosh.query import Term, Or
import json
import re
from collections import defaultdict
from models import ImportedLine


IMPORTER_SETTINGS = 'PROPRIO_IMPORT_PARSERS'


@login_required
def upload(request):
    if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                    data = form.cleaned_data
                    importer = get_element(IMPORTER_SETTINGS, data['type'])
                    parsed_file = importer.parse(data['file'])
                    parsed_file = remove_saved_lines(parsed_file)
                    request.session['import_file'] = parsed_file
                    request.session['import_mapping'] = ['']*len(parsed_file)
                    mapping_url = reverse(mapping)
                    return HttpResponseRedirect(mapping_url)
    else:
            form = UploadForm()
    return render(request,  'bank_import/upload.html', {'form': form})


@login_required
def mapping(request):
    lines = request.session.get('import_file')
    session_mapping = request.session.get('import_mapping')
    # if session has expired
    if lines is None or session_mapping is None:
        url = reverse(upload)
        return HttpResponseRedirect(url)
    session_mapping = [{'mapping': m} for m in session_mapping]
    if request.method == 'POST':
        formset = create_formset(lines, session_mapping, post=request.POST)
        is_valid = formset.is_valid()
        cleaned = [f.cleaned_data.get('mapping') for f in formset]
        if is_valid:
            submit_form(lines, cleaned)
            return redirect(reverse(upload))
        else:
            # store formset_data
            request.session['import_mapping'] = cleaned
    else:
        if request.session['import_mapping'] is None:
            return HttpResponseRedirect(reverse(upload))
        formset = create_formset(lines, session_mapping)
    # formset is necessary for csrf protection
    context = {'zip': zip(lines, formset), 'formset': formset}
    return render(request, 'bank_import/mapping.html', context)


class TenantPaymentMapper:
    type = 'tenant_payment'
    caption = _('Tenant payment')

    def __init__(self):
        tenants = Tenant.objects.all().order_by('name')
        self.tenants = {t.id: t for t in tenants}

    def get_all_values(self):
        return self.tenants.keys()

    def get_caption(self, value):
        return self.tenants[value].name

    def get_long_caption(self, value):
        return u'{}: {}'.format(self.caption, self.get_caption(value))

    def save(self, value, line):
        tenant = self.tenants[value]
        payment = Payment(
            tenant=tenant,
            date=line.date,
            amount=line.amount)
        payment.save()


class TenantNameGuesser:

    def __init__(self):
        tenants = Tenant.objects.all().order_by('name')
        tenant_schema = Schema(name=TEXT(stored=True), id=NUMERIC(stored=True))
        tenant_storage = RamStorage()
        tenant_ix = tenant_storage.create_index(tenant_schema)
        tenant_writer = tenant_ix.writer()
        for t in tenants:
            tenant_writer.add_document(id=t.id, name=t.name.lower())
        tenant_writer.commit()
        self.index = tenant_ix

    def guess(self, line):
        with self.index.searcher() as searcher:
            words = re.split('\W+', line.caption)
            query = Or([Term("name", t.lower()) for t in words])
            result = searcher.search(query)
            matches = [
                (('tenant_payment', r['id'],), r.score,)
                for r in result]
            return matches


mapper_factories = (lambda: TenantPaymentMapper(),)

guesser_factories = (lambda: TenantNameGuesser(),)


def value_to_combo_entry(mapper, value, use_long=False):
    id = json.dumps((mapper.type, value,))
    if use_long:
        caption = mapper.get_caption(value)
    else:
        caption = mapper.get_long_caption(value)
    return (id, caption,)


def guess(guessers, mapper_map, line):
    guesses_map = defaultdict(int)
    for g in guessers:
        guess = g.guess(line)
        for value, score in guess:
            guesses_map[value] += score
    guesses = sorted(guesses_map.items(), key=lambda g: -g[1])
    result = []
    for (mapper_type, value), score in guesses:
        mapper = mapper_map[mapper_type]
        result.append(value_to_combo_entry(mapper, value))
    return result


def create_formset(lines, session_mapping, post=None):
    assert len(session_mapping) == len(lines)
    mappers = [m() for m in mapper_factories]
    mapper_map = {m.type: m for m in mappers}
    guessers = [g() for g in guesser_factories]
    result = []
    for i in range(len(lines)):
        line = lines[i]
        # hardcoded choices
        choices = [
            ('', _('Decide later')),
            ('HIDE', _('Hide line definitively')),
        ]
        # auto choices
        auto_mappings = guess(guessers, mapper_map, line)

        choices.append((_('Automatic mapping'), auto_mappings,))
        # all possible manual mappings
        for m in mappers:
            values = []
            for v in m.get_all_values():
                values.append(value_to_combo_entry(m, v, use_long=True))
            choices.append((m.caption, values,))

        # field value
        if session_mapping[i]['mapping'] != '':
            initial = session_mapping[i]
        elif len(auto_mappings) > 0:
            initial = auto_mappings[0][0]
        else:
            initial = ''
        result.append((choices, initial,))
    init = [{'mapping': i} for (c, i,) in result]
    if post is not None:
        formset = MappingForm(post, initial=init)
    else:
        formset = MappingForm(initial=init)
    for i in range(len(lines)):
        formset[i].fields['mapping'].choices = result[i][0]
    return formset


@transaction.atomic
def submit_form(lines, mappings):
    assert len(lines) == len(mappings)
    mappers = [m() for m in mapper_factories]
    mapper_map = {m.type: m for m in mappers}
    for line, mapping in zip(lines, mappings):
        # skip non-mapped lines
        if mapping == '':
            continue
        # save the mapping to avoid reimporting next time
        line = ImportedLine(
            date=line.date,
            amount=line.amount,
            caption=line.caption,
            mapping=mapping)
        line.save()
        # if this is a simple hide there is nothing more to do
        if mapping == 'HIDE':
            continue
        mapper_type, value = json.loads(mapping)
        mapper = mapper_map[mapper_type]
        mapper.save(value, line)


def remove_saved_lines(lines):
    saved = ImportedLine.objects.all()
    all_ids = set([(l.date, l.amount, l.caption,) for l in saved])
    return [l for l in lines
            if (l.date, l.amount, l.caption,) not in all_ids]
