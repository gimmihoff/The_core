from django.utils import timezone
from ..models import StructureTimer
from ..type_defaults import get_defaults

def apply_type_defaults(structure):
    d = get_defaults(structure.type_id)
    if not d:
        return
    if not structure.type_name and d.get("type_name"):
        structure.type_name = d["type_name"]
    if d.get("nearest"):
        structure.nearest_type = d["nearest"]

def sync_structure_status_from_timers(structure):
    now = timezone.now()
    has_future = StructureTimer.objects.filter(structure=structure, occurs_at__gt=now).exists()
    if has_future and structure.status not in ("DESTROYED", "REMOVED"):
        structure.status = "REINFORCED"
