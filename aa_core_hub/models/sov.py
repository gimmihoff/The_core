from django.db import models
from django.utils import timezone


class SovereigntySystem(models.Model):
    solar_system_id = models.IntegerField(unique=True, db_index=True)
    alliance_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    corporation_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    faction_id = models.IntegerField(null=True, blank=True, db_index=True)
    raw_payload = models.JSONField(null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ("solar_system_id",)
        indexes = [
            models.Index(fields=["alliance_id", "solar_system_id"]),
            models.Index(fields=["corporation_id", "solar_system_id"]),
            models.Index(fields=["faction_id", "solar_system_id"]),
        ]

    def __str__(self) -> str:
        return str(self.solar_system_id)


class SovereigntyStructure(models.Model):
    structure_id = models.BigIntegerField(unique=True, db_index=True)
    structure_type_id = models.IntegerField(null=True, blank=True, db_index=True)
    solar_system_id = models.IntegerField(null=True, blank=True, db_index=True)
    alliance_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    vulnerability_occupancy_level = models.FloatField(null=True, blank=True, db_index=True)
    vulnerable_start_time = models.DateTimeField(null=True, blank=True, db_index=True)
    vulnerable_end_time = models.DateTimeField(null=True, blank=True, db_index=True)
    raw_payload = models.JSONField(null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ("solar_system_id", "structure_id")
        indexes = [
            models.Index(fields=["solar_system_id", "structure_type_id"]),
            models.Index(fields=["alliance_id", "solar_system_id"]),
            models.Index(fields=["vulnerable_start_time", "vulnerable_end_time"]),
        ]

    def __str__(self) -> str:
        return str(self.structure_id)


class SovereigntyCampaign(models.Model):
    campaign_id = models.BigIntegerField(unique=True, db_index=True)
    solar_system_id = models.IntegerField(null=True, blank=True, db_index=True)
    constellation_id = models.IntegerField(null=True, blank=True, db_index=True)
    structure_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    event_type = models.CharField(max_length=64, blank=True, default="", db_index=True)
    defender_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    defender_score = models.FloatField(null=True, blank=True)
    attackers_score = models.FloatField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True, db_index=True)
    raw_payload = models.JSONField(null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ("start_time", "solar_system_id")
        indexes = [
            models.Index(fields=["solar_system_id", "start_time"]),
            models.Index(fields=["constellation_id", "start_time"]),
            models.Index(fields=["defender_id", "start_time"]),
        ]

    def __str__(self) -> str:
        return f"{self.event_type or 'SOV'} {self.solar_system_id or ''}".strip()
