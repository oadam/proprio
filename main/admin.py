from django.contrib import admin
from django.utils.translation import ugettext as _
from main import models

class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_count')

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'building')

class RentRevisionInline(admin.TabularInline):
    model = models.RentRevision
    extra = 1

class PaymentInline(admin.TabularInline):
    model = models.Payment

class FeeInline(admin.TabularInline):
    model = models.Fee
    extra = 1

class TenancyAdmin(admin.ModelAdmin):
    inlines = [
	PaymentInline,
	FeeInline,
        RentRevisionInline,
    ]

admin.site.register(models.Building, BuildingAdmin)
admin.site.register(models.Property, PropertyAdmin)
admin.site.register(models.Tenancy, TenancyAdmin)

