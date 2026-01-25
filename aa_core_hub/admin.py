from django.contrib import admin
from .models import SolarSystemCelestial

@admin.register(SolarSystemCelestial)
class SolarSystemCelestialAdmin(admin.ModelAdmin):
    list_display = ("solar_system_name","celestial_type","name","parent_planet_name")
    list_filter = ("celestial_type","solar_system_name")
    search_fields = ("solar_system_name","name")
