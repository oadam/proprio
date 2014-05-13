from django.contrib import admin
from main.models import Building, Property

class BuildingAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        result = ('name', 'property_count')
        if request.user.is_superuser:
            result = ('user',) + result
        return result
    def get_queryset(self, request):
        qs = super(BuildingAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('user')
        return super(BuildingAdmin, self).get_form(request, obj, **kwargs)
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user
        obj.save()

class PropertyAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        result = ('name', 'address', 'building')
        if request.user.is_superuser:
            result = ('user',) + result
        return result
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "building":
            kwargs["queryset"] = Building.objects.filter(user=request.user)
        return super(PropertyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    def get_queryset(self, request):
        qs = super(PropertyAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('user')
        return super(PropertyAdmin, self).get_form(request, obj, **kwargs)
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user
        obj.save()

admin.site.register(Building, BuildingAdmin)
admin.site.register(Property, PropertyAdmin)

