from esi.clients import EsiClientProvider
from django.db import transaction
from ..models import SolarSystemCelestial

def fetch_system_celestials(system_id: int, system_name: str, overwrite: bool = True) -> int:
    client = EsiClientProvider().client
    system = client.Universe.get_universe_systems_system_id(system_id=system_id).results()

    created = 0
    with transaction.atomic():
        if overwrite:
            SolarSystemCelestial.objects.filter(solar_system_id=system_id).delete()

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
            created += 1

        for p in system.get("planets", []):
            pname = f"P{p.get('index')}"
            SolarSystemCelestial.objects.update_or_create(
                celestial_id=p["planet_id"],
                defaults=dict(
                    solar_system_id=system_id,
                    solar_system_name=system_name,
                    name=pname,
                    celestial_type="PLANET",
                ),
            )
            created += 1

            for idx, m in enumerate(p.get("moons", []), start=1):
                SolarSystemCelestial.objects.update_or_create(
                    celestial_id=m,
                    defaults=dict(
                        solar_system_id=system_id,
                        solar_system_name=system_name,
                        name=f"{pname}M{idx}",
                        celestial_type="MOON",
                        parent_planet_id=p["planet_id"],
                        parent_planet_name=pname,
                    ),
                )
                created += 1

    return created
