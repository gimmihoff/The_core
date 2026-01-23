from django.contrib import admin
from .models import Structure, StructureTimer, DScan, DScanItem, SystemIntel

@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = ("name", "type_name", "standing", "solar_system_name", "owner_alliance_id", "owner_corporation_id", "updated_at")
    list_filter = ("standing", "source")
    search_fields = ("name", "type_name", "solar_system_name")
    ordering = ("-updated_at",)

@admin.register(StructureTimer)
class StructureTimerAdmin(admin.ModelAdmin):
    list_display = ("structure", "phase", "occurs_at", "priority", "is_confirmed")
    list_filter = ("phase", "is_confirmed")
    search_fields = ("structure__name", "structure__solar_system_name")
    ordering = ("occurs_at",)

@admin.register(DScan)
class DScanAdmin(admin.ModelAdmin):
    list_display = ("id", "solar_system_name", "source", "created_by_user_id", "created_at")
    list_filter = ("source",)
    search_fields = ("solar_system_name", "raw_text")
    ordering = ("-created_at",)

@admin.register(DScanItem)
class DScanItemAdmin(admin.ModelAdmin):
    list_display = ("dscan", "name", "type_name", "category", "distance")
    list_filter = ("category",)
    search_fields = ("name", "type_name")
    ordering = ("-id",)

@admin.register(SystemIntel)
class SystemIntelAdmin(admin.ModelAdmin):
    list_display = ("solar_system_name", "solar_system_id", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("solar_system_name", "details")
    ordering = ("solar_system_name",)
