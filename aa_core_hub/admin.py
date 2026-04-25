from django.contrib import admin

from .models import (
    DScan,
    DScanItem,
    EveConstellation,
    EveRegion,
    EveSolarSystem,
    EveStargate,
    SolarSystemCelestial,
    SovereigntyCampaign,
    SovereigntyStructure,
    SovereigntySystem,
    Structure,
    StructureTimer,
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


class StructureTimerInline(admin.TabularInline):
    model = StructureTimer
    extra = 0
    fields = ("phase", "occurs_at", "is_confirmed", "priority", "notes")


@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type_name",
        "structure_category",
        "standing",
        "status",
        "solar_system_name",
        "owner_alliance_id",
        "source",
        "updated_at",
    )
    list_filter = (
        "standing",
        "structure_category",
        "status",
        "fit_status",
        "source",
        "solar_system_name",
    )
    search_fields = (
        "name",
        "type_name",
        "solar_system_name",
        "nearest_name",
        "owner_alliance_id",
        "owner_corporation_id",
    )
    inlines = (StructureTimerInline,)


@admin.register(StructureTimer)
class StructureTimerAdmin(admin.ModelAdmin):
    list_display = ("structure", "phase", "occurs_at", "is_confirmed", "priority")
    list_filter = ("phase", "is_confirmed", "priority", "structure__standing")
    search_fields = ("structure__name", "structure__solar_system_name", "notes")
    autocomplete_fields = ("structure",)


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


@admin.register(SovereigntySystem)
class SovereigntySystemAdmin(admin.ModelAdmin):
    list_display = ("solar_system_id", "alliance_id", "corporation_id", "faction_id", "updated_at")
    list_filter = ("alliance_id", "corporation_id", "faction_id")
    search_fields = ("solar_system_id", "alliance_id", "corporation_id", "faction_id")


@admin.register(SovereigntyStructure)
class SovereigntyStructureAdmin(admin.ModelAdmin):
    list_display = (
        "structure_id",
        "structure_type_id",
        "solar_system_id",
        "alliance_id",
        "vulnerability_occupancy_level",
        "vulnerable_start_time",
        "vulnerable_end_time",
    )
    list_filter = ("structure_type_id", "alliance_id", "solar_system_id")
    search_fields = ("structure_id", "solar_system_id", "alliance_id")


@admin.register(SovereigntyCampaign)
class SovereigntyCampaignAdmin(admin.ModelAdmin):
    list_display = (
        "campaign_id",
        "event_type",
        "solar_system_id",
        "constellation_id",
        "defender_id",
        "start_time",
    )
    list_filter = ("event_type", "defender_id", "solar_system_id")
    search_fields = ("campaign_id", "structure_id", "solar_system_id", "constellation_id")
