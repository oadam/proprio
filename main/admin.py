from django.contrib import admin
from django.utils.translation import ugettext as _
from main import models
from django.core import urlresolvers
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class BuildingFileInline(admin.TabularInline):
    model = models.BuildingFile


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_count')
    inlines = [BuildingFileInline]


class PropertyFileInline(admin.TabularInline):
    model = models.PropertyFile


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'building')
    inlines = [PropertyFileInline]


class RentRevisionInline(admin.TabularInline):
    model = models.RentRevision
    extra = 1


class TenantFileInline(admin.TabularInline):
    model = models.TenantFile
    extra = 1


class PaymentInline(admin.TabularInline):
    model = models.Payment


class FeeInline(admin.TabularInline):
    model = models.Fee
    extra = 1


class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')
    inlines = [
        RentRevisionInline,
        FeeInline,
        TenantFileInline,
        PaymentInline,
    ]
    readonly_fields = ('property_link',)

    def property_link(self, obj):
        url = urlresolvers.reverse(
            'admin:main_property_change', args=(obj.property.id,))
        return format_html(u'<a href={}>{}</a>', mark_safe(url), obj.property)
    property_link.short_description = _('link to the property')

admin.site.register(models.Building, BuildingAdmin)
admin.site.register(models.Property, PropertyAdmin)
admin.site.register(models.Tenant, TenantAdmin)
