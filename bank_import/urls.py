from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.upload),
    url(r'^mapping/$', views.mapping),
)
