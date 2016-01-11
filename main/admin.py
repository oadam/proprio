from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
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

    def building_link(self, obj):
        if obj.building is None:
            return _('No associated building')
        url = urlresolvers.reverse(
            'admin:main_building_change', args=(obj.building.id,))
        return format_html(u'<a href={}>{}</a>', mark_safe(url), obj.building)
    building_link.short_description = _('link to the building')
    readonly_fields = ('building_link',)


class RentRevisionInline(admin.TabularInline):
    model = models.RentRevision
    extra = 1


class TenantFileInline(admin.TabularInline):
    model = models.TenantFile
    extra = 1


class PaymentInline(admin.TabularInline):
    model = models.Payment


class RefundInline(admin.TabularInline):
    model = models.Refund

class FeeInline(admin.TabularInline):
    model = models.Fee
    extra = 1


class DiscountInline(admin.TabularInline):
    model = models.Discount
    extra = 1


class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')
    inlines = [
        RentRevisionInline,
        FeeInline,
        DiscountInline,
        TenantFileInline,
        PaymentInline,
        RefundInline,
    ]
    readonly_fields = ('property_link', 'balance',)

    def property_link(self, obj):
        url = urlresolvers.reverse(
            'admin:main_property_change', args=(obj.property.id,))
        return format_html(u'<a href={}>{}</a>', mark_safe(url), obj.property)
    property_link.short_description = _('link to the property')


# This is a hack to have 2 displays for the tenants
class TenantReminders(models.Tenant):
    class Meta:
        proxy = True
        verbose_name = _("tenant reminder list")
        verbose_name_plural = _("tenants reminder lists")


class ReminderInline(admin.TabularInline):
    fields = ['date', 'read', 'text']
    model = models.Reminder
    extra = 1


class TenantRemindersAdmin(admin.ModelAdmin):
    fields = ('name', 'property')
    readonly_fields = ('name', 'property')
    inlines = [
        ReminderInline,
    ]


admin.site.register(models.Building, BuildingAdmin)
admin.site.register(models.Property, PropertyAdmin)
admin.site.register(models.Tenant, TenantAdmin)
admin.site.register(TenantReminders, TenantRemindersAdmin)
