from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms import UploadForm
from django.http import HttpResponseRedirect


@login_required
def upload3(request):
    if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                    data = form.cleaned_data
                    if data['type'] != 'CIC':
                        raise 'yo'
                    
                    return HttpResponseRedirect('/thanks/')
    else:
            form = UploadForm()
    return render(request,  'bank_import/upload.html', {'form': form})
