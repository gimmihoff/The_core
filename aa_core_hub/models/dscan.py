import uuid

from django.db import models
from django.utils import timezone


class DScan(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    source = models.CharField(max_length=32, default="MANUAL", db_index=True)
    solar_system_id = models.IntegerField(null=True, blank=True, db_index=True)
    solar_system_name = models.CharField(max_length=128, blank=True, default="", db_index=True)
    raw_text = models.TextField()
    parsed_json = models.JSONField(null=True, blank=True)
    created_by_user_id = models.IntegerField(null=True, blank=True, db_index=True)
    scanned_at = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ("-scanned_at", "-created_at")
        indexes = [
            models.Index(fields=["public_id", "created_at"]),
            models.Index(fields=["solar_system_id", "scanned_at"]),
            models.Index(fields=["solar_system_name", "scanned_at"]),
            models.Index(fields=["source", "scanned_at"]),
        ]


class DScanItem(models.Model):
    dscan = models.ForeignKey(DScan, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255, db_index=True)
    type_name = models.CharField(max_length=255, blank=True, default="", db_index=True)
    distance = models.CharField(max_length=64, blank=True, default="")
    category = models.CharField(max_length=64, blank=True, default="", db_index=True)

    class Meta:
        indexes = [models.Index(fields=["type_name", "category"])]
