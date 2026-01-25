from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import StructureTimer
from .services.structure_logic import sync_structure_status_from_timers

@receiver([post_save, post_delete], sender=StructureTimer)
def _sync_structure_status(sender, instance, **kwargs):
    s = instance.structure
    sync_structure_status_from_timers(s)
    s.save(update_fields=["status", "updated_at"])
