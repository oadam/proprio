from django.conf import settings
from django.views import static
from django.contrib.auth.decorators import login_required


@login_required
def serve_static(request, path, **kwargs):
    """this is copy/pasted/modified from
    django/views.py to add @login_required"""
    return static.serve(
        request, path,
        document_root=settings.MEDIA_ROOT, **kwargs)
