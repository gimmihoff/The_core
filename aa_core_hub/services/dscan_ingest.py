from django.db import transaction
from django.utils import timezone

from ..models import DScan, DScanItem
from .dscan_parser import parse_dscan


def create_dscan(
    *,
    raw_text: str,
    solar_system_id: int,
    solar_system_name: str = "",
    source: str = "MANUAL",
    created_by_user_id: int | None = None,
    scanned_at=None,
) -> DScan:
    """Create a D-scan and normalized item rows for child upload apps."""

    if not raw_text or not raw_text.strip():
        raise ValueError("raw_text is required")
    if not solar_system_id:
        raise ValueError("solar_system_id is required to link a D-scan to a system")

    parsed_items = parse_dscan(raw_text)
    scanned_at = scanned_at or timezone.now()

    with transaction.atomic():
        dscan = DScan.objects.create(
            source=source or "MANUAL",
            solar_system_id=solar_system_id,
            solar_system_name=solar_system_name or "",
            raw_text=raw_text,
            parsed_json=parsed_items,
            created_by_user_id=created_by_user_id,
            scanned_at=scanned_at,
        )
        DScanItem.objects.bulk_create(
            [
                DScanItem(
                    dscan=dscan,
                    name=item["name"],
                    type_name=item["type_name"],
                    distance=item["distance"],
                    category=item.get("category", ""),
                )
                for item in parsed_items
            ]
        )
    return dscan


def get_dscan_timeline_for_system(*, solar_system_id: int, limit: int = 100):
    """Return recent D-scans for a system, ordered for timeline displays."""

    if not solar_system_id:
        raise ValueError("solar_system_id is required")
    return (
        DScan.objects.filter(solar_system_id=solar_system_id)
        .prefetch_related("items")
        .order_by("-scanned_at", "-created_at")[:limit]
    )
