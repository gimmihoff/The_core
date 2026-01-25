from django.contrib import admin
from .models import Structure, StructureTimer, DScan, DScanItem, SystemIntel

@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = ("name","type_id","type_name","standing","status","solar_system_name","nearest_type","nearest_name","fit_status","updated_at")
    list_filter = ("standing","status","nearest_type","source")
    search_fields = ("name","type_name","solar_system_name")
    ordering = ("-updated_at",)

@admin.register(StructureTimer)
class StructureTimerAdmin(admin.ModelAdmin):
    list_display = ("structure","phase","occurs_at","priority","is_confirmed")
    list_filter = ("phase","is_confirmed")
    ordering = ("occurs_at",)

@admin.register(DScan)
class DScanAdmin(admin.ModelAdmin):
    list_display = ("id","solar_system_name","source","created_at")
    list_filter = ("source",)
    ordering = ("-created_at",)

@admin.register(DScanItem)
class DScanItemAdmin(admin.ModelAdmin):
    list_display = ("dscan","name","type_name","category","distance")
    list_filter = ("category",)
    ordering = ("-id",)

@admin.register(SystemIntel)
class SystemIntelAdmin(admin.ModelAdmin):
    list_display = ("solar_system_name","solar_system_id","status","updated_at")
    list_filter = ("status",)
    ordering = ("solar_system_name",)
