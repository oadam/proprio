from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth.views import logout
import re

admin.autodiscover()

media_regex = r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/'))
urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='main/', permanent=True)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('main.urls')),
    url(r'^import/', include('bank_import.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', lambda request: logout(request, '/')),
    url(media_regex, 'proprio.views.serve_static'),
)
