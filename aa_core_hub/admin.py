from django.contrib import admin

from .models import DScan, DScanItem, SolarSystemCelestial


class DScanItemInline(admin.TabularInline):
    model = DScanItem
    extra = 0
    fields = ("name", "type_name", "distance", "category")
    readonly_fields = fields
    can_delete = False


@admin.register(DScan)
class DScanAdmin(admin.ModelAdmin):
    list_display = ("solar_system_name", "solar_system_id", "source", "scanned_at", "created_at")
    list_filter = ("source", "solar_system_name")
    search_fields = ("solar_system_name", "raw_text", "items__name", "items__type_name")
    readonly_fields = ("created_at",)
    inlines = (DScanItemInline,)


@admin.register(SolarSystemCelestial)
class SolarSystemCelestialAdmin(admin.ModelAdmin):
    list_display = ("solar_system_name", "celestial_type", "name", "parent_planet_name")
    list_filter = ("celestial_type", "solar_system_name")
    search_fields = ("solar_system_name", "name")
