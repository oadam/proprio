from django.contrib import admin
from django.utils.translation import ugettext as _
from main.models import Building, Property, Tenancy, RentRevision

class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_count')

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'building')

class RentRevisionInline(admin.TabularInline):
    model = RentRevision

class TenancyAdmin(admin.ModelAdmin):
    inlines = [
        RentRevisionInline
    ]

admin.site.register(Building, BuildingAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Tenancy, TenancyAdmin)

