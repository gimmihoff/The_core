from django.db import transaction

from ..models import EveConstellation, EveRegion, EveSolarSystem, EveStargate


def upsert_region(*, region_id: int, name: str, description: str = "") -> EveRegion:
    region, _ = EveRegion.objects.update_or_create(
        region_id=region_id,
        defaults={
            "name": name,
            "description": description or "",
        },
    )
    return region


def upsert_constellation(
    *,
    constellation_id: int,
    name: str,
    region_id: int | None = None,
) -> EveConstellation:
    region = EveRegion.objects.filter(region_id=region_id).first() if region_id else None
    constellation, _ = EveConstellation.objects.update_or_create(
        constellation_id=constellation_id,
        defaults={
            "name": name,
            "region": region,
            "region_id_external": region_id,
        },
    )
    return constellation


def upsert_solar_system(
    *,
    solar_system_id: int,
    name: str,
    constellation_id: int | None = None,
    region_id: int | None = None,
    security_status: float | None = None,
    position: dict | None = None,
) -> EveSolarSystem:
    constellation = (
        EveConstellation.objects.filter(constellation_id=constellation_id).first()
        if constellation_id
        else None
    )
    region = EveRegion.objects.filter(region_id=region_id).first() if region_id else None
    position = position or {}
    system, _ = EveSolarSystem.objects.update_or_create(
        solar_system_id=solar_system_id,
        defaults={
            "name": name,
            "constellation": constellation,
            "constellation_id_external": constellation_id,
            "region": region,
            "region_id_external": region_id,
            "security_status": security_status,
            "position_x": position.get("x"),
            "position_y": position.get("y"),
            "position_z": position.get("z"),
        },
    )
    return system


def upsert_stargate(
    *,
    stargate_id: int,
    source_system_id: int,
    name: str = "",
    destination_stargate_id: int | None = None,
    destination_system_id: int | None = None,
    position: dict | None = None,
) -> EveStargate:
    source_system = EveSolarSystem.objects.filter(solar_system_id=source_system_id).first()
    destination_system = (
        EveSolarSystem.objects.filter(solar_system_id=destination_system_id).first()
        if destination_system_id
        else None
    )
    position = position or {}
    stargate, _ = EveStargate.objects.update_or_create(
        stargate_id=stargate_id,
        defaults={
            "name": name or "",
            "source_system": source_system,
            "source_system_id_external": source_system_id,
            "destination_stargate_id": destination_stargate_id,
            "destination_system": destination_system,
            "destination_system_id_external": destination_system_id,
            "position_x": position.get("x"),
            "position_y": position.get("y"),
            "position_z": position.get("z"),
        },
    )
    return stargate


def get_system_context(*, solar_system_id: int) -> dict:
    if not solar_system_id:
        raise ValueError("solar_system_id is required")

    system = (
        EveSolarSystem.objects.select_related("constellation", "region")
        .filter(solar_system_id=solar_system_id)
        .first()
    )
    if not system:
        return {}

    gates = EveStargate.objects.filter(source_system_id_external=solar_system_id).select_related(
        "destination_system"
    )
    return {
        "system": system,
        "constellation": system.constellation,
        "region": system.region,
        "stargates": list(gates),
        "neighbor_system_ids": [
            gate.destination_system_id_external
            for gate in gates
            if gate.destination_system_id_external
        ],
    }


def get_neighbor_systems(*, solar_system_id: int):
    context = get_system_context(solar_system_id=solar_system_id)
    neighbor_ids = context.get("neighbor_system_ids", [])
    return EveSolarSystem.objects.filter(solar_system_id__in=neighbor_ids).order_by("name")


def fetch_system_geography(system_id: int):
    """Populate Core's map cache for one system and its outgoing stargates via ESI."""

    from esi.clients import EsiClientProvider

    client = EsiClientProvider().client
    system_data = client.Universe.get_universe_systems_system_id(system_id=system_id).results()
    constellation_id = system_data.get("constellation_id")
    constellation_data = (
        client.Universe.get_universe_constellations_constellation_id(
            constellation_id=constellation_id
        ).results()
        if constellation_id
        else {}
    )
    region_id = constellation_data.get("region_id")
    region_data = (
        client.Universe.get_universe_regions_region_id(region_id=region_id).results()
        if region_id
        else {}
    )

    with transaction.atomic():
        if region_id:
            upsert_region(
                region_id=region_id,
                name=region_data.get("name", ""),
                description=region_data.get("description", ""),
            )
        if constellation_id:
            upsert_constellation(
                constellation_id=constellation_id,
                name=constellation_data.get("name", ""),
                region_id=region_id,
            )
        system = upsert_solar_system(
            solar_system_id=system_id,
            name=system_data.get("name", ""),
            constellation_id=constellation_id,
            region_id=region_id,
            security_status=system_data.get("security_status"),
            position=system_data.get("position"),
        )
        for stargate_id in system_data.get("stargates", []):
            stargate_data = client.Universe.get_universe_stargates_stargate_id(
                stargate_id=stargate_id
            ).results()
            destination = stargate_data.get("destination") or {}
            upsert_stargate(
                stargate_id=stargate_id,
                source_system_id=system_id,
                name=stargate_data.get("name", ""),
                destination_stargate_id=destination.get("stargate_id"),
                destination_system_id=destination.get("system_id"),
                position=stargate_data.get("position"),
            )
    return system
