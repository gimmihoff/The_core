from django.db import models
from django.utils import timezone
from ..constants import (
    FIT_STATUS,
    NEAREST_TYPES,
    STRUCTURE_CATEGORIES,
    STRUCTURE_STANDINGS,
    STRUCTURE_STATUS,
)

class Structure(models.Model):
    type_id = models.IntegerField(null=True, blank=True, db_index=True)
    type_name = models.CharField(max_length=255, blank=True, default="", db_index=True)
    structure_category = models.CharField(
        max_length=32,
        choices=STRUCTURE_CATEGORIES,
        default="UNKNOWN",
        db_index=True,
    )
    structure_id = models.BigIntegerField(null=True, blank=True, db_index=True, unique=True)

    name = models.CharField(max_length=255, db_index=True)
    standing = models.CharField(max_length=16, choices=STRUCTURE_STANDINGS, default="NEUTRAL", db_index=True)

    owner_corporation_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    owner_alliance_id = models.BigIntegerField(null=True, blank=True, db_index=True)

    solar_system_id = models.IntegerField(null=True, blank=True, db_index=True)
    solar_system_name = models.CharField(max_length=128, blank=True, default="", db_index=True)
    constellation_id = models.IntegerField(null=True, blank=True, db_index=True)
    constellation_name = models.CharField(max_length=128, blank=True, default="")
    region_id = models.IntegerField(null=True, blank=True, db_index=True)
    region_name = models.CharField(max_length=128, blank=True, default="")

    nearest_type = models.CharField(max_length=16, choices=NEAREST_TYPES, default="ANYWHERE", db_index=True)
    nearest_name = models.CharField(max_length=64, blank=True, default="", db_index=True)

    status = models.CharField(max_length=16, choices=STRUCTURE_STATUS, default="UNKNOWN", db_index=True)
    fit_status = models.CharField(max_length=16, choices=FIT_STATUS, default="UNKNOWN", db_index=True)

    reinforce_hour = models.TimeField(null=True, blank=True, db_index=True)
    reinforce_effective_from = models.DateTimeField(null=True, blank=True, db_index=True)

    source = models.CharField(max_length=32, default="MANUAL", db_index=True)
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
            models.Index(fields=["type_id", "standing"]),
            models.Index(fields=["structure_category", "standing"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.type_name or self.type_id or 'Unknown'})"
