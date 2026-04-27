from django.utils import timezone

from ..models import SovereigntyCampaign, SovereigntyStructure, SovereigntySystem


def upsert_sov_system(payload: dict) -> SovereigntySystem:
    system, _ = SovereigntySystem.objects.update_or_create(
        solar_system_id=payload["system_id"],
        defaults={
            "alliance_id": payload.get("alliance_id"),
            "corporation_id": payload.get("corporation_id"),
            "faction_id": payload.get("faction_id"),
            "raw_payload": payload,
            "updated_at": timezone.now(),
        },
    )
    return system


def upsert_sov_structure(payload: dict) -> SovereigntyStructure:
    structure, _ = SovereigntyStructure.objects.update_or_create(
        structure_id=payload["structure_id"],
        defaults={
            "structure_type_id": payload.get("structure_type_id"),
            "solar_system_id": payload.get("solar_system_id"),
            "alliance_id": payload.get("alliance_id"),
            "vulnerability_occupancy_level": payload.get("vulnerability_occupancy_level"),
            "vulnerable_start_time": payload.get("vulnerable_start_time"),
            "vulnerable_end_time": payload.get("vulnerable_end_time"),
            "raw_payload": payload,
            "updated_at": timezone.now(),
        },
    )
    return structure


def upsert_sov_campaign(payload: dict) -> SovereigntyCampaign:
    campaign_id = payload.get("campaign_id") or payload.get("event_id")
    if not campaign_id:
        raise ValueError("campaign_id or event_id is required")

    campaign, _ = SovereigntyCampaign.objects.update_or_create(
        campaign_id=campaign_id,
        defaults={
            "solar_system_id": payload.get("solar_system_id"),
            "constellation_id": payload.get("constellation_id"),
            "structure_id": payload.get("structure_id"),
            "event_type": payload.get("event_type") or "",
            "defender_id": payload.get("defender_id"),
            "defender_score": payload.get("defender_score"),
            "attackers_score": payload.get("attackers_score"),
            "start_time": payload.get("start_time"),
            "raw_payload": payload,
            "updated_at": timezone.now(),
        },
    )
    return campaign


def get_sov_context(*, solar_system_id: int) -> dict:
    if not solar_system_id:
        raise ValueError("solar_system_id is required")

    return {
        "system": SovereigntySystem.objects.filter(solar_system_id=solar_system_id).first(),
        "structures": list(
            SovereigntyStructure.objects.filter(solar_system_id=solar_system_id).order_by(
                "structure_type_id",
                "structure_id",
            )
        ),
        "campaigns": list(
            SovereigntyCampaign.objects.filter(solar_system_id=solar_system_id).order_by(
                "start_time"
            )
        ),
    }


def fetch_sovereignty_map() -> int:
    from esi.clients import EsiClientProvider

    client = EsiClientProvider().client
    rows = client.Sovereignty.get_sovereignty_map().results()
    for row in rows:
        upsert_sov_system(row)
    return len(rows)


def fetch_sovereignty_structures() -> int:
    from esi.clients import EsiClientProvider

    client = EsiClientProvider().client
    rows = client.Sovereignty.get_sovereignty_structures().results()
    for row in rows:
        upsert_sov_structure(row)
    return len(rows)


def fetch_sovereignty_campaigns() -> int:
    from esi.clients import EsiClientProvider

    client = EsiClientProvider().client
    rows = client.Sovereignty.get_sovereignty_campaigns().results()
    for row in rows:
        upsert_sov_campaign(row)
    return len(rows)
