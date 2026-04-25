"""Public child-plugin API for AA Core Hub.

Child plugins should import supported models and helper functions from this
module instead of reaching into internal package modules.
"""

from .models import (
    DScan,
    DScanItem,
    EveConstellation,
    EveRegion,
    EveSolarSystem,
    EveStargate,
    SolarSystemCelestial,
    Structure,
    StructureTimer,
    SystemIntel,
)
from .services.dscan_parser import parse_dscan
from .services.dscan_ingest import create_dscan, get_dscan_timeline_for_system
from .services.geography import (
    get_neighbor_systems,
    get_system_context,
    upsert_constellation,
    upsert_region,
    upsert_solar_system,
    upsert_stargate,
)
from .services.structure_logic import apply_type_defaults, sync_structure_status_from_timers
from .type_defaults import get_defaults


def fetch_system_celestials(system_id: int, system_name: str, overwrite: bool = True) -> int:
    """Populate the celestial cache for a solar system via ESI.

    The ESI client import stays lazy so the rest of the child-plugin API remains
    importable in environments that do not have AllianceAuth's ESI integration
    loaded yet.
    """

    from .services.celestial_fetch import fetch_system_celestials as _fetch_system_celestials

    return _fetch_system_celestials(
        system_id=system_id,
        system_name=system_name,
        overwrite=overwrite,
    )


def fetch_system_geography(system_id: int):
    """Populate Core's region, constellation, system, and stargate cache via ESI."""

    from .services.geography import fetch_system_geography as _fetch_system_geography

    return _fetch_system_geography(system_id=system_id)


__all__ = [
    "DScan",
    "DScanItem",
    "EveConstellation",
    "EveRegion",
    "EveSolarSystem",
    "EveStargate",
    "SolarSystemCelestial",
    "Structure",
    "StructureTimer",
    "SystemIntel",
    "apply_type_defaults",
    "create_dscan",
    "fetch_system_celestials",
    "fetch_system_geography",
    "get_neighbor_systems",
    "get_dscan_timeline_for_system",
    "get_defaults",
    "get_system_context",
    "parse_dscan",
    "sync_structure_status_from_timers",
    "upsert_constellation",
    "upsert_region",
    "upsert_solar_system",
    "upsert_stargate",
]
