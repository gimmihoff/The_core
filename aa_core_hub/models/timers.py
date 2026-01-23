from django.db import models
from django.utils import timezone
from ..constants import TIMER_PHASES

class StructureTimer(models.Model):
    """Timer model used by timer boards and war-planning tooling."""
    structure = models.ForeignKey("aa_core_hub.Structure", on_delete=models.CASCADE, related_name="timers")

    phase = models.CharField(max_length=16, choices=TIMER_PHASES, default="OTHER", db_index=True)
    occurs_at = models.DateTimeField(db_index=True)

    # optional metadata
    is_confirmed = models.BooleanField(default=False, db_index=True)
    priority = models.PositiveSmallIntegerField(default=3, db_index=True)  # 1=highest
    notes = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("occurs_at",)
        indexes = [
            models.Index(fields=["occurs_at", "phase"]),
            models.Index(fields=["priority", "occurs_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.structure} - {self.phase} @ {self.occurs_at}"
