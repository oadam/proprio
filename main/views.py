from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import Tenant
import json


@login_required
def tenants(request):
    result = []
    for t in Tenant.objects.all().order_by('name'):
        if t.balance() < 0:
            css = "danger"
        else:
            css = ""
        rounded_trend = [round(v, 2) for v in t.trend()]
        result.append({
            "tenant": t,
            "css": css,
            "normal_min": json.dumps(float(t.rent())),
            "trend": json.dumps(rounded_trend)
        })
    context = {'tenants': result}
    return render(request, 'main/tenants.html', context)


@login_required
def tenant_cashflows(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    context = {'cashflows': tenant.cashflows()}
    return render(request, 'main/cashflows.html', context)
