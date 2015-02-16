from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import Tenant
import json


@login_required
def tenants(request):
    result = []
    tenants = (
        Tenant.objects.all()
        .prefetch_related('reminder_set')
        .order_by('name'))
    for t in tenants:
        rounded_trend = [round(v, 2) for v in t.trend()]
        current_trend = rounded_trend[-1]
        float_rent = float(t.rent())
        if current_trend < -1.2 * float_rent:
            css = "danger"
        elif current_trend < -0.2 * float_rent:
            css = "warning"
        else:
            css = ""
        result.append({
            "tenant": t,
            "css": css,
            "normal_min": json.dumps(float_rent),
            "trend": json.dumps(rounded_trend)
        })
    context = {'tenants': result}
    return render(request, 'main/tenants.html', context)


@login_required
def tenant_cashflows(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    context = {'cashflows': tenant.cashflows()}
    return render(request, 'main/cashflows.html', context)
