from esi.clients import EsiClientProvider
from ..models import SolarSystemCelestial

def fetch_system_celestials(system_id: int, system_name: str):
    client = EsiClientProvider().client
    system = client.Universe.get_universe_systems_system_id(system_id=system_id).results()

    # planets and moons
    for p in system.get("planets", []):
        planet_id = p.get("planet_id")
        SolarSystemCelestial.objects.update_or_create(
            celestial_id=planet_id,
            defaults=dict(
                solar_system_id=system_id,
                solar_system_name=system_name,
                name=f"P{p.get('index')}",
                celestial_type="PLANET",
            ),
        )
        for m in p.get("moons", []):
            SolarSystemCelestial.objects.update_or_create(
                celestial_id=m,
                defaults=dict(
                    solar_system_id=system_id,
                    solar_system_name=system_name,
                    name=f"P{p.get('index')}M{p.get('moons', []).index(m)+1}",
                    celestial_type="MOON",
                    parent_planet_id=planet_id,
                    parent_planet_name=f"P{p.get('index')}",
                ),
            )

    # star
    star_id = system.get("star_id")
    if star_id:
        SolarSystemCelestial.objects.update_or_create(
            celestial_id=star_id,
            defaults=dict(
                solar_system_id=system_id,
                solar_system_name=system_name,
                name="Sun",
                celestial_type="STAR",
            ),
        )
