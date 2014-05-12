from django.contrib import admin
from main.models import Building, Property

class PropertyInline(admin.TabularInline):
    model = Property

class BuildingAdmin(admin.ModelAdmin):
    inlines = [PropertyInline]
    list_display = ('address', 'property_count')
    def get_queryset(self, request):
        qs = super(BuildingAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

admin.site.register(Building, BuildingAdmin)

