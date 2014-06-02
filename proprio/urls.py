from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth.views import logout

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='main/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('main.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', lambda request: logout(request, '/')),
)
