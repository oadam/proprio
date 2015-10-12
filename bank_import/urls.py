from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.forms),
    url(r'^generate-mapping$', views.generate),
    url(r'^submit-mapping$', views.submit),
)
