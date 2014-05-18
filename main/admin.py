from django.contrib import admin
from main.models import Building, Property

class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_count')

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'building')

admin.site.register(Building, BuildingAdmin)
admin.site.register(Property, PropertyAdmin)

