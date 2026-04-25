from django.contrib import admin

from .models import (
    DScan,
    DScanItem,
    EveConstellation,
    EveRegion,
    EveSolarSystem,
    EveStargate,
    SolarSystemCelestial,
)


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


@admin.register(EveRegion)
class EveRegionAdmin(admin.ModelAdmin):
    list_display = ("name", "region_id")
    search_fields = ("name", "region_id")


@admin.register(EveConstellation)
class EveConstellationAdmin(admin.ModelAdmin):
    list_display = ("name", "constellation_id", "region_id_external", "region")
    list_filter = ("region",)
    search_fields = ("name", "constellation_id", "region__name")


@admin.register(EveSolarSystem)
class EveSolarSystemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "solar_system_id",
        "security_status",
        "constellation_id_external",
        "region_id_external",
    )
    list_filter = ("region", "constellation")
    search_fields = ("name", "solar_system_id", "constellation__name", "region__name")


@admin.register(EveStargate)
class EveStargateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "stargate_id",
        "source_system_id_external",
        "destination_system_id_external",
    )
    search_fields = (
        "name",
        "stargate_id",
        "source_system__name",
        "destination_system__name",
    )
