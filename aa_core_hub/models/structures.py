from django.db import models
from django.utils import timezone
from ..constants import STRUCTURE_STANDINGS

class Structure(models.Model):
    """Canonical structure record used by all child plugins."""

    # ESI structure id (may be null for manual entries / non-ESI entities)
    structure_id = models.BigIntegerField(null=True, blank=True, db_index=True, unique=True)

    name = models.CharField(max_length=255, db_index=True)
    type_name = models.CharField(max_length=255, blank=True, default="")
    standing = models.CharField(max_length=16, choices=STRUCTURE_STANDINGS, default="NEUTRAL", db_index=True)

    # Ownership
    owner_corporation_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    owner_alliance_id = models.BigIntegerField(null=True, blank=True, db_index=True)

    # Location
    solar_system_id = models.IntegerField(null=True, blank=True, db_index=True)
    solar_system_name = models.CharField(max_length=128, blank=True, default="", db_index=True)
    constellation_id = models.IntegerField(null=True, blank=True, db_index=True)
    constellation_name = models.CharField(max_length=128, blank=True, default="")
    region_id = models.IntegerField(null=True, blank=True, db_index=True)
    region_name = models.CharField(max_length=128, blank=True, default="")

    # Metadata
    source = models.CharField(max_length=32, default="MANUAL", db_index=True)  # MANUAL, ESI, IMPORT, etc.
    notes = models.TextField(blank=True, default="")
    last_seen_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)
        indexes = [
            models.Index(fields=["solar_system_id", "standing"]),
            models.Index(fields=["owner_alliance_id", "standing"]),
            models.Index(fields=["owner_corporation_id", "standing"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.type_name})"
