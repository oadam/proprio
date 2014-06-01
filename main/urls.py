from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.tenants),
    url(r'^tenant-cashflows/(?P<tenant_id>\d+)/$', views.tenant_cashflows, name="tenant_cashflows"),
)
