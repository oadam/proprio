from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.tenants, name="tenants"),
    url(r'^tenant-cashflows/(?P<tenant_id>\d+)/$',
        views.tenant_cashflows, name="tenant_cashflows"),
    url(r'^tenant-reminders/(?P<tenant_id>\d+)/$',
        views.tenant_reminders, name="tenant_reminders"),
)
