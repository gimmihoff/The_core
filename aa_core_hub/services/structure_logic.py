from django.utils import timezone

from ..models import Structure, StructureTimer
from ..type_defaults import get_defaults


def classify_structure_category(type_name: str = "", type_id: int | None = None) -> str:
    normalized = (type_name or "").lower()
    if any(term in normalized for term in ("territorial claim unit", "infrastructure hub", "ihub")):
        return "SOV"
    if any(term in normalized for term in ("cyno beacon", "cyno jammer", "ansiblex", "jump gate")):
        return "FLEX"
    if "customs office" in normalized:
        return "CUSTOMS_OFFICE"
    if "skyhook" in normalized:
        return "SKYHOOK"
    if any(term in normalized for term in ("metenox", "moon drill")):
        return "MOON_DRILL"
    if "mercenary den" in normalized:
        return "MERCENARY_DEN"
    if type_name or type_id:
        return "STRUCTURE"
    return "UNKNOWN"


def apply_type_defaults(structure):
    d = get_defaults(structure.type_id)
    if not d:
        return
    if not structure.type_name and d.get("type_name"):
        structure.type_name = d["type_name"]
    if d.get("nearest"):
        structure.nearest_type = d["nearest"]
    if structure.structure_category == "UNKNOWN":
        structure.structure_category = classify_structure_category(
            type_name=structure.type_name,
            type_id=structure.type_id,
        )


def sync_structure_status_from_timers(structure):
    now = timezone.now()
    has_future = StructureTimer.objects.filter(structure=structure, occurs_at__gt=now).exists()
    if has_future and structure.status not in ("DESTROYED", "REMOVED"):
        structure.status = "REINFORCED"


def create_or_update_structure(
    *,
    name: str,
    standing: str = "HOSTILE",
    type_id: int | None = None,
    type_name: str = "",
    structure_category: str = "UNKNOWN",
    structure_id: int | None = None,
    owner_corporation_id: int | None = None,
    owner_alliance_id: int | None = None,
    solar_system_id: int | None = None,
    solar_system_name: str = "",
    constellation_id: int | None = None,
    constellation_name: str = "",
    region_id: int | None = None,
    region_name: str = "",
    nearest_type: str = "ANYWHERE",
    nearest_name: str = "",
    status: str = "UNKNOWN",
    fit_status: str = "UNKNOWN",
    reinforce_hour=None,
    reinforce_effective_from=None,
    source: str = "MANUAL",
    notes: str = "",
    last_seen_at=None,
) -> Structure:
    """Create or update a structure using the Core war-planning contract."""

    if not name or not name.strip():
        raise ValueError("name is required")

    lookup = {"structure_id": structure_id} if structure_id else {"name": name.strip()}
    structure, _ = Structure.objects.update_or_create(
        **lookup,
        defaults={
            "name": name.strip(),
            "standing": standing or "HOSTILE",
            "type_id": type_id,
            "type_name": type_name or "",
            "structure_category": structure_category
            if structure_category and structure_category != "UNKNOWN"
            else classify_structure_category(type_name=type_name, type_id=type_id),
            "owner_corporation_id": owner_corporation_id,
            "owner_alliance_id": owner_alliance_id,
            "solar_system_id": solar_system_id,
            "solar_system_name": solar_system_name or "",
            "constellation_id": constellation_id,
            "constellation_name": constellation_name or "",
            "region_id": region_id,
            "region_name": region_name or "",
            "nearest_type": nearest_type or "ANYWHERE",
            "nearest_name": nearest_name or "",
            "status": status or "UNKNOWN",
            "fit_status": fit_status or "UNKNOWN",
            "reinforce_hour": reinforce_hour,
            "reinforce_effective_from": reinforce_effective_from,
            "source": source or "MANUAL",
            "notes": notes or "",
            "last_seen_at": last_seen_at or timezone.now(),
        },
    )
    apply_type_defaults(structure)
    structure.save()
    return structure


def create_enemy_structure(**kwargs) -> Structure:
    """Shortcut for adding hostile structures from upload/intel child apps."""

    kwargs["standing"] = "HOSTILE"
    return create_or_update_structure(**kwargs)


def create_structure_timer(
    *,
    structure: Structure,
    occurs_at,
    phase: str = "OTHER",
    is_confirmed: bool = False,
    priority: int = 3,
    notes: str = "",
) -> StructureTimer:
    if not structure:
        raise ValueError("structure is required")
    if not occurs_at:
        raise ValueError("occurs_at is required")

    timer = StructureTimer.objects.create(
        structure=structure,
        phase=phase or "OTHER",
        occurs_at=occurs_at,
        is_confirmed=is_confirmed,
        priority=priority,
        notes=notes or "",
    )
    sync_structure_status_from_timers(structure)
    structure.save(update_fields=["status", "updated_at"])
    return timer


def get_war_timer_timeline(
    *,
    solar_system_id: int | None = None,
    standing: str = "HOSTILE",
    include_unconfirmed: bool = True,
    limit: int = 100,
):
    qs = StructureTimer.objects.select_related("structure").filter(occurs_at__gte=timezone.now())
    if standing:
        qs = qs.filter(structure__standing=standing)
    if solar_system_id:
        qs = qs.filter(structure__solar_system_id=solar_system_id)
    if not include_unconfirmed:
        qs = qs.filter(is_confirmed=True)
    return qs.order_by("occurs_at", "priority")[:limit]
