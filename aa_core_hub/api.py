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
    SovereigntyCampaign,
    SovereigntyStructure,
    SovereigntySystem,
    Structure,
    StructureTimer,
    SystemIntel,
)
from .services.dscan_parser import parse_dscan
from .services.dscan_ingest import (
    create_dscan,
    get_dscan_by_public_id,
    get_dscan_timeline_for_system,
)
from .services.geography import (
    fetch_constellation_geography,
    fetch_region_geography,
    get_neighbor_systems,
    get_system_context,
    upsert_constellation,
    upsert_region,
    upsert_solar_system,
    upsert_stargate,
)
from .services.sov import (
    get_sov_context,
    upsert_sov_campaign,
    upsert_sov_structure,
    upsert_sov_system,
)
from .services.structure_logic import (
    apply_type_defaults,
    classify_structure_category,
    create_enemy_structure,
    create_or_update_structure,
    create_structure_timer,
    get_war_timer_timeline,
    sync_structure_status_from_timers,
)
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


def fetch_sovereignty_map() -> int:
    from .services.sov import fetch_sovereignty_map as _fetch_sovereignty_map

    return _fetch_sovereignty_map()


def fetch_sovereignty_structures() -> int:
    from .services.sov import fetch_sovereignty_structures as _fetch_sovereignty_structures

    return _fetch_sovereignty_structures()


def fetch_sovereignty_campaigns() -> int:
    from .services.sov import fetch_sovereignty_campaigns as _fetch_sovereignty_campaigns

    return _fetch_sovereignty_campaigns()


__all__ = [
    "DScan",
    "DScanItem",
    "EveConstellation",
    "EveRegion",
    "EveSolarSystem",
    "EveStargate",
    "SolarSystemCelestial",
    "SovereigntyCampaign",
    "SovereigntyStructure",
    "SovereigntySystem",
    "Structure",
    "StructureTimer",
    "SystemIntel",
    "apply_type_defaults",
    "classify_structure_category",
    "create_dscan",
    "create_enemy_structure",
    "create_or_update_structure",
    "create_structure_timer",
    "fetch_system_celestials",
    "fetch_constellation_geography",
    "fetch_region_geography",
    "fetch_system_geography",
    "fetch_sovereignty_campaigns",
    "fetch_sovereignty_map",
    "fetch_sovereignty_structures",
    "get_neighbor_systems",
    "get_dscan_by_public_id",
    "get_dscan_timeline_for_system",
    "get_defaults",
    "get_system_context",
    "get_sov_context",
    "get_war_timer_timeline",
    "parse_dscan",
    "sync_structure_status_from_timers",
    "upsert_constellation",
    "upsert_region",
    "upsert_solar_system",
    "upsert_sov_campaign",
    "upsert_sov_structure",
    "upsert_sov_system",
    "upsert_stargate",
]
